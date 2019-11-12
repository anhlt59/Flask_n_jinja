""" macro for option 
    macro func() define function for set options
    macro load() get options in __main__ script
"""

# function
{% macro func(data_input) %}
{% if data_input['option']|length >0-%}
def option_parser():
    """Options"""
    parser = OptionParser()
    {%- for i in data_input['option'] -%}
    {%- if i is string -%}
    {{options(i)|safe}}
    {%- elif i is mapping %}
    {{def_option(i)|safe}}
    {%- endif-%}
    {%-endfor %}
    options, args = parser.parse_args()
    # required option
    for option in ({%for i in data_input['list_option']-%}
        {%-if data_input['list_option']['Default'] != '' %}'{{i|safe}}'
        {%- if loop.index < data_input['list_option']|length%}, {%endif%}
        {%- endif %}{% endfor -%}):
        if not getattr(options, option):
            print 'Option %s not specified' % option
            parser.print_help()
            sys.exit(UNKNOWN)
    return options
{% endif %}
{% endmacro %}


# invoke function option_parser()
{%- macro load(data_input) -%}
    {%-if data_input['option']|length >0-%}
    # options
    options = option_parser()
    {%-endif-%}
{% endmacro -%}


# customize template
{% macro def_option(option) -%}
    parser.add_option("{{option.option}}", dest="{{option.dest}}", type="{{option.type}}",Default="{{option.Default}}",
                            help="{{option.help}}", metavar='{{option.metavar}}')
{% endmacro -%}

# available template
{% macro options(key) -%}
    {%- if key == 'host' -%}
    {# macro for host #}
    parser.add_option("-H", dest="host", type="string",
                            help="Hostname/IP Address of device", metavar=' ')
    {%- elif key == 'community' -%}
    {# macro for community #}
    parser.add_option("-c", "-C", dest="community", type="string",
                            help="Community string", metavar=' ')
    {%- elif key == 'hostname' -%}
    {# macro for hostname #}
    parser.add_option("-t", dest="hostname", type="string",
                            help="Host name", metavar=' ', default='')
    {%- elif key == 'ifindex' -%}
    {# macro for ifindex #}
    parser.add_option("-k", dest="ifindex", type="string",
                            help="SNMP ifIndex", metavar=' ')
    {%- elif key == 'throughput' -%}
    {# macro for throughput #}
    parser.add_option("--throughput", dest="throughput", type="string", default="0,0",
                            help="Traffic warning, critical threshold in %. Default 0,0)", metavar=' ')
    {%- elif key == 'error' -%}
    {# macro for error #}
    parser.add_option("--error", dest="error", type="string", default="0,0",
                            help="CRC per minute warning,critical threshold Default 0,0", metavar=' ')
    {%- elif key == 'discard' -%}
    {# macro for discard #}
    parser.add_option("--discard", dest="discard", type="string", default="0,0",
                            help="Discard per minute warning,critical threshold. Default 0,0", metavar=' ')
    {%- elif key == 'speed' -%}
    {# macro for speed #}
    parser.add_option("--speed", dest="speed", type="string", default="auto",
                            help="Discard per minute warning,critical threshold. Default 0 (auto-detect)", metavar=' ')
    {%- elif key == 'perfdata' -%}
    {# macro for perfdata #}
    parser.add_option("-p", dest="perfdata", action="store_true", default=False,
                            help="Enable performance data", metavar=' ')
    {%- elif key == 'lastcheck' -%}
    {# macro for lastcheck #}
    parser.add_option("-l", dest="lastcheck", type="int", default=0,
                            help="Last_check e.g. 0=OK, 1=WARNING, 2=CRITICAL, 3=UNKNOWN", metavar=' ')
    {%- elif key == 'peer' -%}
    {# macro for peer #}
    parser.add_option("--peer", dest="peer", type="string",
                            help="peer IP", metavar=' ')
    {%- elif key == 'advlimit' -%}
    {# macro for advlimit #}
    parser.add_option("--advlimit", dest="advlimit", type="int",
                            help="Advertised Prefix Threshold", metavar=' ')
    {%- elif key == 'warning' -%}
    {# macro for warning #}
    parser.add_option("-w", "-W", dest="warning", type="string",
                            help="threshold Warning", metavar=' ')
    {%- elif key == 'critical' -%}
    {# macro for critical #}
    parser.add_option("-t", "-T", dest="critical", type="string",
                            help="threshold Critical", metavar=' ')
    {%- elif key == 'bandwidth' -%}
    {# macro for bandwidth #}
    parser.add_option("-b", dest="bandwidth", type="string",
                            help="bandwidth threshold", metavar=' ')
    {%- endif -%}
{% endmacro -%}