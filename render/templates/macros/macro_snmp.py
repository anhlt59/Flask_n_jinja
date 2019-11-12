""" get/walk snmp
    macro func() define function to get/walk snmp
    macro input() get snmp in __main__ script
"""

# function get/walk snmp
{% macro func(data_input) %}
{# get snmp -#}
{% if data_input['get_snmp_var']|length > 0 -%}
{{get_snmp(data_input)}}
{% endif -%}
{# walk snmp -#}
{% if data_input['walk_snmp_var']|length > 0 -%}
{{walk_snmp(data_input)}}
{% endif %}
{% endmacro %}

# invoke function get/walk snmp
{% macro load(data_input) -%}
    {# get snmp -#}
    {% if data_input['get_snmp_var']|length > 0 -%}
    # get snmp
    get_result = get_snmp()
    {% endif -%}
    {# walk snmp -#}
    {% if data_input['walk_snmp_var']|length > 0 -%}
    # walk snmp
    walk_result = walk_snmp()
    {% endif -%}
{% endmacro -%}
 


# get snmp
{% macro get_snmp(data_input) -%}
def get_snmp():
    """Get SNMP"""   
    sess = netsnmp.Session(Version={{data_input.snmp.Version}}, DestHost={{data_input.snmp.DestHost}},
                           Community={{data_input.snmp.Community}}, Timeout={{data_input.snmp.Timeout}}, Retries={{data_input.snmp.Retries}})
    {% for i in data_input['oid']['get'] -%}
    {{i['var']|safe}} = {{i['value']|safe}}
    {% endfor -%}
    vars =  netsnmp.VarList(
        {% for i in data_input['get_snmp_var'] -%}
        {{i|safe}}{%if loop.index < data_input['get_snmp_var']|length%}, {%endif%}
        {% endfor -%}
        )
    return sess.get(vars)
{% endmacro -%}
# walk snmp
{% macro walk_snmp(data_input) -%}
{% if data_input['oid']['walk']|length > 0  -%}
def walk_snmp():
    """Walk SNMP"""
    {% for i in data_input['oid']['walk'] -%}
    {{i['var']|safe}} = netsnmp.snmpwalk({{i['value']|safe}}, Version={{data_input.snmp.Version}}, DestHost={{data_input.snmp.DestHost}},
                           Community={{data_input.snmp.Community}}, Timeout={{data_input.snmp.Timeout}}, Retries={{data_input.snmp.Retries}})
    {% endfor -%}
    return [{% for i in data_input['walk_snmp_var'] -%}{{i|safe}}{%if loop.index < data_input['walk_snmp_var']|length%}, {%endif%}{% endfor -%}]
{% endif -%}
{% endmacro -%}

# index snmp 
{% macro index(name,reference) -%}
{% for OID in reference -%}
    {% if name == OID  -%}{{loop.index0}}{% endif -%}
{% endfor -%}
{% endmacro -%}
