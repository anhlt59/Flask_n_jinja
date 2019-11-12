{% import 'macros/macro_option.py' as option -%}
{% import 'macros/macro_kibana.py' as kibana -%}
{% import 'macros/macro_last.py' as last -%}
{% import 'macros/macro_set_var.py' as set_var -%}
{% import 'macros/macro_library.py' as library -%}
{% import 'macros/macro_condition.py' as condition -%}
{% extends 'template_script.py' -%}

{# library #}
{% block library %}
{{super}}
{{library.func(data_input)}}
{% endblock %}

{# function #}
{% block function %}
{# function for set option #}
{{option.func(data_input)}}
{# function for get kibana log #}
{{kibana.func(data_input)}}
{# function for load/save data #}
{{last.func(data_input)}}
{# function for check output #}
{{condition.func()}}
{% endblock %}

{# main #}
{# input #}
{% block input %}
    {# option #}
    {{option.load(data_input)}}
    {# snmp #}
    {{kibana.load(data_input)}}
    {# last #}
    {{last.load(data_input)}}
{% endblock %}

{# set_var #}
{% block variable %}
    {{set_var.var(data_input)}
    {# save data #}
    {{last.save(data_input)}}
{% endblock %}

{# condition #}
{% block condition %}
    {{condition.main(data_input)}}
{% endblock %}