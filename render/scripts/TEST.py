#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from os import path, chmod, mkdir
import re
from optparse import OptionParser
import netsnmp
import cPickle

def option_parser():
    """Options"""
    parser = OptionParser()
    parser.add_option("-H", dest="host", type="string",
                            help="Hostname/IP Address of device", metavar=' ')
    parser.add_option("-c", "-C", dest="community", type="string",
                            help="Community string", metavar=' ')
    parser.add_option("-k", dest="ifindex", type="string",
                            help="SNMP ifIndex", metavar=' ')
    options, args = parser.parse_args()
    # required option
    for option in ('host', 'community', 'ifindex'):
        if not getattr(options, option):
            print 'Option %s not specified' % option
            parser.print_help()
            sys.exit(UNKNOWN)
    return options

def walk_snmp():
    """Walk SNMP"""
    jnxOperatingTemp = netsnmp.snmpwalk(.1.3.6.1.4.1.2636.3.1.13.1.7.7, Version=2, DestHost=options.host,
                           Community=options.community, Timeout=5000000, Retries=3)
    jnxOperatingDescr = netsnmp.snmpwalk(.1.3.6.1.4.1.2636.3.1.13.1.5.7, Version=2, DestHost=options.host,
                           Community=options.community, Timeout=5000000, Retries=3)
    return [jnxOperatingTemp, jnxOperatingDescr]

class Data():
    """ Class for load/save data"""
    def __init__(self):
        self.dir_path = path.dirname(path.abspath(__file__))
        self.script_name = path.splitext(path.basename(__file__))[0]
        self.script_path = path.join(self.dir_path, self.script_name)
        self.filename = path.join(self.script_path, str(options.host) + ".tmp")
        self.f_exist()
    # create folder/ file if not exists
    def f_exist(self):    
        if not path.isdir(self.script_path):
            try:
                mkdir(self.script_path, 0777)
            except Exception as e:
                print "UNKNOWN - mkdir:  %s" % e
                sys.exit(UNKNOWN)
        if not path.exists(self.filename):
            try:
                open(self.filename, 'wb')
            except Exception as e:
                print "UNKNOWN - mkdir:  %s" % e
                sys.exit(UNKNOWN)   
    # Save data
    def save(self, *data):
        chmod(self.filename, 0777)
        with open(self.filename, 'wb') as f:
            cPickle.dump(data, f)   
    # Load data 
    def load(self):
        with open(self.filename, 'rb') as f:
            try:
                return cPickle.load(f)
            except:
                return [None, None, None]

def output(stt, status, message):
    """Check status"""
    if status == stt:
        print {0: 'OK', 1: 'WARNING', 2: 'CRITICAL', 3: 'UNKNOWN'}[status] + ': ' + message
        sys.exit(status)

if __name__ == '__main__':
    # Exit statuses recognized by Nagios
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    # options
    options = option_parser()

    # walk snmp
    walk_result = walk_snmp()

    # load data
    Data = Data()
    last_result = Data.load()

    # set vars
    jnxOperatingTemp = list(walk_result[0])
    jnxOperatingDescr = list(walk_result[1])
    regDesc = [re.findall(r'(FPC:\s*(\S*).*\@\s*(\d+))', x, re.I) for x in jnxOperatingDescr]
    type_device = list([x[0][1] for x in regDesc])
    number = list([int(x[0][2]) for x in regDesc])
    regTemp = [re.findall(r'(\d+)', x, re.I) for x in jnxOperatingTemp]
    temp = list([x[0] for x in regTemp])
    temp1 = list([x_2+x_1 for (x_1, x_2) in zip(type_device, temp+number) if x_1== 'MPCE'])
    x_1 = list([len(temp) + lem(x) - 10 for x in number])
    x2 = list(last_result[0] - 10)
    x3 = list(last_result[1]-last_result[0] - 10)
    x2 = list(last_result[2] - 10)

    # save data
    Data.save(number, regTemp, temp)

    # CONDITION
    status = OK
    message = ''

    # CRITICAL
    for (x_1, x_2) in zip(number, temp):
        if x_2> 46:
            status = CRITICAL
            message = str(message)+    '[FPC '   + str(x_1)+   ''   + str(x_2)+    '%]'
    output(CRITICAL, status, message)
    # WARNING
    for (x_1, x_2) in zip(number, temp):
        if 42 <x_2<= 46:
            status = WARNING
            message = str(message)+    '[FPC '   + str(x_1)+   ''   + str(x_2)+    '%]'
    output(WARNING, status, message)
    # OK
    if status == OK:
        status = OK
        for (x_1, x_2) in zip(number, temp):
            message = str(message)+    '[FPC '   + str(x_1)+   ' '   + str(x_2)+    '%]'
    output(OK, status, message)
