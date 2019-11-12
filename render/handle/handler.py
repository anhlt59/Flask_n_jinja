"""Handler input script."""
# !/usr/bin/python
# library
import re
from module import *


def modify(data_input, FORM_DATA):
    """Modify input."""
    d = init_data(data_input, FORM_DATA)
    # them data input vars
    for i in range(len(d['vars'])):
        # check regex
        if d['vars'][i]['type'] == 'regex':
            if d['vars'][i]['cond'] in d['type_is_list'] or re.match(r'^list(.+)$'\
                                                    , d['vars'][i]['cond'], re.I):
                d['type_is_list'].append(d['vars'][i]['var'])
                d['regex_var'].append(d['vars'][i]['var'])
            d['vars'][i]['val'] = "re.findall(r'("+ d['vars'][i]['val'] +")', " +\
                                                d['vars'][i]['cond']+', re.I)'
            d['vars'][i]['cond'] = ''

        val, cond = modify_var(d, d['vars'][i], ['val', 'cond'])

        if d['vars'][i]['type'] == 'list':
            d['type_is_list'].append(d['vars'][i]['var'])

        # check err var
        if not re.match(r'^[a-zA-Z0-9_]+$', d['vars'][i]['var'].strip()):
            d['err'] += 'Invalid var: ' + d['vars'][i]['var'] + '\n'
        # check err cond, val
        validate_variable(d, cond, val)
        d['all_var'] |= {(d['vars'][i]['var'])}

        # check loop
        id = get_loop_id(d, check_loop_1(d,cond),check_loop_1(d,val))
        d['vars'][i].update({'val':val,'cond':cond,'id':id})
        final_str(d['vars'][i],([0,'cond'],[1, 'val']))

    # them data input condition-message
    for x in ['UNKNOWN','CRITICAL','WARNING','OK']:
        for i in range(len(d[x])):
            cond, msg = modify_var(d, d[x][i], ['cond', 'msg'])
            validate_condition(d,cond, msg)
            # check loop
            id = get_loop_id(d, check_loop_1(d,cond),check_loop_1(d,msg))
            d[x][i].update({'cond':cond,'msg':msg,'id':id})
            # modify string msg
            final_str(d[x][i], ([0,'cond'],[1, 'msg']))

    # import thu vien cho script
    import_lib(d)
    return d
