{% from 'macros/macro_snmp.py' import index %}

""" set condition 
"""

# function to check status
{% macro func(data_input)%}
def output(stt, status, message):
    """Check status"""
    if status == stt:
        print {0: 'OK', 1: 'WARNING', 2: 'CRITICAL', 3: 'UNKNOWN'}[status] + ': ' + message
        sys.exit(status)

{% endmacro %}

# condition main
{% macro main(data_input) -%}
    {# CONDITION#}
    # CONDITION
    {% if not 'status' in data_input['all_var'] -%}
    status = OK
    {% endif -%}
    message = ''
{% for x in ['UNKNOWN', 'CRITICAL', 'WARNING', 'OK']-%}
{% if data_input[x]|length > 0 -%}
{% for i in range(data_input[x]|length) -%}
    {#status#}
    # {{x}}
    {{cond(data_input[x][i]['id'][0], data_input[x][i], x,data_input)}}
{%- endfor %}
    output({{x}}, status, message)
{% endif -%}
{% endfor -%}

{%- endmacro -%}


# id 0 khong co var list
{% macro cond(id, cond_msg,status,data_input)-%}
{% if id == 0 -%}
    if {{cond_msg['cond']|safe}}:
        {# status -#}
        status = {{status}}
        {# message -#}
        message = {{cond_msg['msg']|safe}}


# id 1 co var list trong msg
{%- elif id == 1 -%}
    if {{cond_msg['cond']|safe}}:
        {# status -#}
        status = {{status}}
        {# 1 list var -#}
        {% if cond_msg['id'][1][2]|length == 1 -%}
        for x in {{cond_msg['id'][1][2][0]}}:
            message = {{cond_msg['msg']|safe}}
        {# 2 list var -#}
        {%- elif cond_msg['id'][1][2]|length == 2 -%}
        for (x_1, x_2) in zip({{cond_msg['id'][1][2][0]}}, {{cond_msg['id'][1][2][1]}}):
            message = {{cond_msg['msg']|safe}}
        {# 3 list var -#}
        {%- elif cond_msg['id'][1][2]|length == 3 -%}
        for (x_1, x_2, x_3) in zip({{cond_msg['id'][1][2][0]}}, {{cond_msg['id'][1][2][1]}}, , {{cond_msg['id'][1][2][1]}}):
            message = {{cond_msg['msg']|safe}}
        {%-endif-%}


{# id 2, co var list trong condition #}
{# id 3, co var list trong condition va msg tuong tu macro cond_2() #}
{%- elif id == 2 or id == 3-%}
    {# 1 list var -#}
    {% if cond_msg['id'][1][2]|length == 1 -%}
    for x in {{cond_msg['id'][1][2][0]}}:
        if {{cond_msg['cond']|safe}}:
            status = {{status}}
            message = {{cond_msg['msg']|safe}}
    {# 2 list var -#}
    {%- elif cond_msg['id'][1][2]|length == 2 -%}
    for (x_1, x_2) in zip({{cond_msg['id'][1][2][0]}}, {{cond_msg['id'][1][2][1]}}):
        if {{cond_msg['cond']|safe}}:
            status = {{status}}
            message = {{cond_msg['msg']|safe}}
    {# 3 list var -#}
    {%- elif cond_msg['id'][1][2]|length == 3 -%}
    for (x_1, x_2, x_3) in zip({{cond_msg['id'][1][2][0]}}, {{cond_msg['id'][1][2][1]}}, {{cond_msg['id'][1][2][2]}}):
        if {{cond_msg['cond']|safe}}:
            status = {{status}}
            message = {{cond_msg['msg']|safe}}
    {%-endif-%}
{%- endif -%}
{%- endmacro -%}

