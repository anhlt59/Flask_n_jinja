"""File config."""
# !/usr/bin/python
# library
from os import path
from sys import path as syspath

# path
ROOT_PATH = path.dirname(path.abspath(__file__))
SCRIPT_PATH = path.join(ROOT_PATH, 'scripts')
HANDLE_PATH = path.join(ROOT_PATH, 'handle')
TEMPLATE_PATH = path.join(ROOT_PATH, 'templates')
syspath.extend([SCRIPT_PATH, HANDLE_PATH])

# form input
FORM_DATA = {
    'name': '',
    'err': '',
    'library': set(),
    'all_var': set(),
    'get_snmp_var': [],
    'walk_snmp_var': [],
    'list_option': [],
    'regex_var': [],
    'type_is_list': [],
    'list_last': [],
    'oid': {},
    'option': [],
    'snmp': {},
    'vars': [],
    'UNKNOWN': [],
    'CRITICAL': [],
    'WARNING': [],
    'OK': []
}

TEST = {
    'name': 'TEST',
    'option': [
        'host',
        'community',
        'ifindex'
    ],
    'snmp': {'Version': 2, 'DestHost': 'options.host', 'Retries': 3,
             'Community': 'options.community', 'Timeout': 5000000},
    'oid': {
        'get': [
        ],
        'walk': [
            {'var': 'jnxOperatingTemp',
             'value': '.1.3.6.1.4.1.2636.3.1.13.1.7.7'},
            {'var': 'jnxOperatingDescr',
             'value': ".1.3.6.1.4.1.2636.3.1.13.1.5.7"}
        ]
    },
    'vars': [
        {'var': 'jnxOperatingTemp', 'type': 'list',
         'val': 'snmp.jnxOperatingTemp', 'cond': ''},
        {'var': 'jnxOperatingDescr', 'type': 'list',
         'val': 'snmp.jnxOperatingDescr', 'cond': ""},
        {'var': 'regDesc', 'type': 'regex',
         'val': 'FPC:\\s*(\\S*).*\\@\\s*(\\d+)', 'cond': 'jnxOperatingDescr'},
        {'var': 'type_device', 'type': 'list',
         'val': 'regDesc\\\\0\\\\1', 'cond': ''},
        {'var': 'number', 'type': 'list',
         'val': 'int(regDesc\\\\0\\\\2)', 'cond': ''},
        {'var': 'regTemp', 'type': 'regex',
         'val': '\\d+', 'cond': 'jnxOperatingTemp'},
        {'var': 'temp', 'type': 'list',
                        'val': 'regTemp\\\\0', 'cond': ''},
        {'var': 'temp1', 'type': 'list', 'val': 'temp|number + type_device',
         'cond': 'type_device ==\'MPCE\''},
        {'var': 'x_1', 'type': 'list',
         'val': 'len(temp) + lem(number) - 10', 'cond': ''},
        {'var': 'x2', 'type': 'list',
         'val': 'last.number - 10', 'cond': ''},
        {'var': 'x3', 'type': 'list',
         'val': 'last.regTemp-last.number - 10', 'cond': ''},
        {'var': 'x2', 'type': 'list',
         'val': 'last.temp - 10', 'cond': ''},

    ],
    'OK': [
        {'cond': 'status == OK',
         'msg': 'message + \'[FPC \'+ number +" "+ temp + \'%]\' '}
    ],
    'WARNING': [
        {'cond': '42 < temp <= 46',
         'msg': 'message + \'[FPC \'+ number +""+ temp + \'%]\' '},
    ],
    'CRITICAL': [
        {'cond': 'temp > 46',
         'msg': 'message + \'[FPC \'+ number +""+ temp + \'%]\' '},
    ],
    'UNKNOWN': [],
}
