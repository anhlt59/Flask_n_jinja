# !/usr/bin/python
# library
import re
import ast
from functools import reduce


def init_data(d, form_data):
    """Init data_input."""
    form_data.update(d)
    form_data['get_snmp_var'] = [x['var'] for x in d['oid']['get']]
    form_data['walk_snmp_var'] = [x['var'] for x in d['oid']['walk']]
    form_data['list_option'] = [x['dest'] if type(x) == dict
                                else x for x in d['option']]
    return form_data


def import_lib(d):
    """Import library after modify input."""
    # option
    if len(d['option']) > 0:
        d['library'] |= {'from optparse import OptionParser'}
    # snmp
    if len(d['oid']['get']) + len(d['oid']['walk']) > 0:
        d['library'] |= {'import netsnmp'}
        # check err if not host, community
        if not {'host', 'community'} <= set(d['list_option']):
            d['err'] += 'Missing options for snmp\n'
    # time
    if 'time' in d:
        d['library'] |= {'import time'}
    # regex
    if len(d['regex_var']) > 0:
        d['library'] |= {'import re'}
    # last
    if len(d['list_last']) > 0:
        d['library'] |= {'import cPickle', 'from os import path, chmod, mkdir'}


def modify_var(d, var):
    """Replace snmp, last, options, time (ex: smmp.oid_1 --> get_result[1])."""
    # match regex
    if var['type'] == 'regex':
        # chuyển sang cú pháp python sử dụng findall()
        val = "re.findall(r'(" + var['val'] + ")', " + var['cond'] + ', re.I)'
        var.update({'val': val, 'cond': ''})
        return var
    # call regex
    if '\\\\' in var['val']:
        # (ex:reg\\0\\1 check bien reg có phải regex dc khai báo)
        call_regex = set(re.findall(r'(?<!\\)[0-9a-zA-Z_]+(?=\\)', val))
        if not call_regex <= set(d['regex_var']):
            d['err'] += 'Regex err: ' + str(call_regex - set(d['regex_var']))\
                        .replace('{', '').replace('}', '\n')
        # chuyển sang cú pháp python
        val = re.sub(r'\\\\(\d+|\w+)', lambda x: '[' + x.group(1) + ']', val)
        var.update({'val': val})
        return var
    # check value snmp, last, time, options
    for arg in args:
        group = var[arg].replace("\"", "\'").split('\'')
        # ex var = str_1 + 'high temperture' => ignor 'high temperture'
        for i in range(0, len(group), 2):
            grs = re.findall(r'(\w+)\.([0-9a-zA-Z_]+)', var[arg], re.I)
            for gr in grs:
                # snmp
                if gr[0].lower() == 'snmp':
                    # snmp get
                    if gr[1] in d['get_snmp_var']:
                        d['all_var'] |= {'get_result[{}]'.format(
                                         str(d['get_snmp_var'].index(gr[1])))}
                        group[i] = re.sub(r'snmp.({})'.format(gr[1]),
                            lambda x: 'get_result[{}]'.format(str(
                            d['get_snmp_var'].index(x.group(1)))), group[i])
                    # snmp walk
                    elif gr[1] in d['walk_snmp_var']:
                        d['all_var'] |= {'walk_result[{}]'.format(
                                         str(d['walk_snmp_var'].index(gr[1])))}
                        d['type_is_list'].append('walk_result[{}]'.format(
                            str(d['walk_snmp_var'].index(gr[1]))))
                        group[i] = re.sub(r'snmp.({})'.format(gr[1]),
                            lambda x: 'walk_result[{}]'.format(str(
                            d['walk_snmp_var'].index(x.group(1)))), group[i])
                    else:
                        if 'Unknown snmp: {}\n'.format(gr[1]) not in d['err']:
                            d['err'] += 'Unknown snmp: {}\n'.format(gr[1])
                # last
                if gr[0].lower() == 'last':
                    # add list_last
                    if gr[1] not in d['list_last']:
                        d['list_last'].append(gr[1])
                        d['all_var'] |= {'last_result[{}]'.format(
                            str(d['list_last'].index(gr[1])))}
                        if gr[1] in d['type_is_list']:
                            d['type_is_list'].append('last_result[{}]'.format(
                                str(d['list_last'].index(gr[1]))))
                    if gr[1] in d['list_last']:
                        group[i] = re.sub(r'last.({})'.format(gr[1]),
                            lambda x: 'last_result[{}]'.format(
                            str(d['list_last'].index(x.group(1)))), group[i])
                    if gr[1] not in d['all_var']:
                        if 'Unknown last: {}\n'.format(gr[1]) not in d['err']:
                            d['err'] += 'Unknown last: {}\n'.format(gr[1])
                # time
                if gr[0].lower() == 'time':
                    d['time'] = 1
                    if gr[1] == 'digit':
                        group[i] = group[i].replace(
                            'time.digit', 'time.time()')
                    elif gr[1] == 'string':
                        group[i] = group[i].replace(
                            'time.string', "time.strftime('%X')")
                    elif gr[1] == 'date':
                        group[i] = group[i].replace(
                            'time.date', "time.strftime('%x')")
                    else:
                        if 'Unknow time: {}\n'.format(gr[1]) not in d['err']:
                            d['err'] += 'Unknow time: {}\n'.format(gr[1])
                # options
                if gr[0].lower() == 'options':
                    if gr[1] not in d['list_option']:
                        if 'Unknow option: {}\n'.format(gr[1]) not in d['err']:
                            d['err'] += 'Unknow option: {}\n'.format(gr[1])
        var.update({arg:(''.join([group[i] if i % 2 == 0 else '\'{}\''.format(
            group[i]) for i in range(len(group))])).strip()})
    return var


def check_regex(d, var):
    # Handle REGEX.
    # match regex
    if var['type'] == 'regex':
        # chuyển sang cú pháp python sử dụng findall()
        val = "re.findall(r'(" + var['val'] + ")', " + var['cond'] + ', re.I)'
        var.update({'val': val, 'cond': ''})
        return var
    # call regex
    if '\\\\' in var['val']:
        # (ex:reg\\0\\1 check bien reg có phải regex dc khai báo)
        call_regex = set(re.findall(r'(?<!\\)[0-9a-zA-Z_]+(?=\\)', val))
        if not call_regex <= set(d['regex_var']):
            d['err'] += 'Regex err: ' + str(call_regex - set(d['regex_var']))\
                        .replace('{', '').replace('}', '\n')
        # chuyển sang cú pháp python
        val = re.sub(r'\\\\(\d+|\w+)', lambda x: '[' + x.group(1) + ']', val)
        var.update({'val': val})
        return var
# replace cac bien theo form


def final_str(var, value):
    for (x, y) in value:
        var[y] = var[y].replace('|', '+').replace('^',
                                                  '**').replace("\"", "\'")
        for i in range(len(var['id'][1][2])):
            for j in var['id'][1][x]:
                if j == var['id'][1][2][i]:
                    if ", re.I)" not in var[y]:
                        j_2 = re.sub(
                            r'\+|\-|\*|\/|\(|\)|\^|\[|\]|\.', lambda x: '\\'+x.group(), j)
                        reg = r"(?<=\+|\-|\*|\/|\.|\[|\(|\^|\=|\>|\<|\!)\s*{}\s*(?=\!|\+|\-|\^|\*|\/|\.|\[|\)|\=|\>|\<)|^{}\s*(?=\!|\+|\-|\*|\/|\.|\^|\[|\(|\=|\>|\<)|(?<=\!|\+|\-|\*|\/|\.|\[|\(|\=|\>|\<)\s*{}$|^{}$"\
                            .format(j_2, j_2, j_2, j_2)
                        list_str = var[y].split('\'')
                        for k in range(0, len(list_str), 2):
                            list_str[k] = re.sub(reg, lambda x: 'x', list_str[k]) if len(var['id'][1][2])\
                                == 1 else re.sub(reg, lambda x: 'x_'+str(i+1), list_str[k])
                        for k in range(1, len(list_str), 2):
                            list_str[k] = '\'{}\''.format(list_str[k])
                        var[y] = ' '.join(list_str).strip()
                    else:
                        reg = r"{}(?=,\sre.I)".format(j)
                        var[y] = re.sub(reg, lambda x: 'x', var[y]) if len(var['id'][1][2])\
                            == 1 else re.sub(reg, lambda x: 'x_'+str(i+1), var[y])
    if y == 'msg':
        list_str = var[y].split('\'')
        for i in range(0, len(list_str), 2):
            list_str[i] = re.sub(r'((^(?<!str\()[a-zA-Z0-9_\[\]\(\)\.]+)\s*(?=\+))|((?<=\+)\s*(?!str\()[a-zA-Z0-9_\[\]\(\)\.]+)|((^(?<!str\()[a-zA-Z0-9_\[\]\(\)\.]+)$)',
                                 lambda x: ' str('+x.group().strip()+')', list_str[i])
        for i in range(1, len(list_str), 2):
            list_str[i] = '\'{}\''.format(list_str[i])
        var[y] = ' '.join(list_str).strip()
    return var

# check method is used


def str_count(string, method):
    var = []
    for j in range(string.count(method)):
        while method in string:
            index = string.find(method)
            if index != -1:
                for x in range(index, len(string)):
                    if string[index:x+1].count('(') == string[index:x+1].count(')')\
                            and string[index:x+1].count('(') != 0:
                        var.append(string[index:x+1])
                        string = string.replace(string[index:x+1], '1')
                        break
        return var, string


def check_method(d, string):
    """check method is support."""
    method = set(re.findall(r'[a-zA-Z0-9_]+(?=\()', string))
    method_support = {'zip', 'replace', 'range', 'tuple', 'set', 'list', 'str',
                      'strftime', 'sorted', 'int', 'float', 'type', 'round',
                      'len', 'cmp', 'max', 'min', 'index', 'pop', 'count',
                      'remove', 'findall', 'time'}
    if not method < method_support:
        d['err'] += 'Method is not supported: ' + str(method - method_support).\
            replace('{', '').replace('}', '') + '\n'
    return method

# exception for method return none list



def check_loop_1(d, string):
    var = set()
    string = string.split('\'')
    string = '1'.join([string[i] for i in range(0, len(string), 2)])
    for i in check_method(d, string) & {'len', 'cmp', 'max', 'min', 'index', 'pop', 'count', 'remove'}:
        result = str_count(string, i)
        string = result[1]
    return string


def check_loop_2(d, string):
    """Exception for method return list."""
    var = set()
    while '|' in string:
        reg = re.search(r'[a-zA-Z0-9_]+\s*\||\[[^\]]+\]\s*\|', string)
        if reg:
            str_var = reg.group()
            string = string[string.find(str_var):].replace(str_var, '', 1)
        while True:
            reg_var = re.match(r'\s*[a-zA-Z0-9_]+|\s*\[[^\]]+\]', string)
            if reg_var:
                str_var += reg_var.group()
                string = string.replace(reg_var.group(), '', 1)
            reg_stop = re.match(r'\s*\|+', string)
            if reg_stop:
                str_var += reg_stop.group()
                string = string.replace(reg_stop.group(), '', 1)
            else:
                var |= {str_var}
                break
    for i in (check_method(d, string) & {'zip', 'range', 'tuple', 'set', 'list', 'sorted'}):
        result = str_count(string, i)
        var |= set(result[0])
    return list(var)

# check var_iterate in string


def get_loop_id(d, *string):
    string = list(string)
    list_exception = [check_loop_2(d, i) for i in string]
    for i in range(len(string)):
        for j in sorted(list_exception[i], key=lambda x: len(x), reverse=True):
            if j in string[i]:
                string[i] = string[i].replace(j, 'var_iterate')
            else:
                list_exception[i].remove(j)
            list_exception[i] = [x.replace('|', '+')
                                 for x in list_exception[i]]
    var = [filter_var(i) for i in string]
    for x in range(len(var)):
        var[x] = [i for i in var[x] if i in d['type_is_list'] +
                  d['walk_snmp_var']] + list_exception[x]
    if string[1] == 'var_iterate' or string[1] in d['all_var']:
        var[1] = []
    var.append(sorted(list(set(var[0]) | set(var[1])),
                      key=lambda x: len(x), reverse=True))
    if string[0] == 'var_iterate':
        var[0] = []
    # var[0] var_iterate for agr_1, var[1] var_iterate for agr_2, var[2] total var_iterate
    if len(var[0]) == 0:
        return (0, var) if len(var[1]) == 0 else (1, var)
    else:
        return (2, var) if len(var[1]) == 0 else (3, var)


def filter_var(*string):
    """filter var in string."""
    reg, result = [], []
    for i in string:
        reg += re.findall(r'(\w+)\(', i)
        result += [x[0]
                   for x in re.findall(r'((walk|get|last)_result\[\d+\])', i)]
    return reduce(lambda x, y: x | y, [set([node.id for node in ast.walk(
        ast.parse(i)) if isinstance(node, ast.Name)]) for i in string])\
        - set(reg)


def validate(f):
    """Decorator for check err."""
    def wrapper(d, var, *string):
        var = [x for x in filter_var(*string) if '_result[' not in x]
        err = f(d, var, *string)
        if len(err) != 0:
            d['err'] += 'Variable is not defined: ' + str(err).\
                replace('{', '').replace('}', '\n')
    return wrapper


@validate
def validate_var(d, var, *string):
    """check validate variables in string set var."""
    return set(var) - {'walk_result', 'get_result', 'last_result', 'time',
'snmp', 'last', 'options', 'time', 're'} - d['all_var']


@validate
def validate_condition(d, var, *string):
    """check validate variables in string condition."""
    return set(var) - {'walk_result', 'get_result', 'snmp', 'last', 'options', 'time', 'UNKNOWN',
                       'CRITICAL', 'WARNING', 'OK', 'message', 'status'} - d['all_var']
