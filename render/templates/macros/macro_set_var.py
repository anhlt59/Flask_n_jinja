{% from 'macros/macro_snmp.py' import index -%}
""" set variables in __main__
"""

# set_var main
{% macro main(data_input) %}
    {%if data_input['vars']|length > 0-%}
    # set vars
    {% for i in range(data_input['vars']|length) -%}
    {{var(data_input['vars'][i], data_input)}}
    {% endfor -%}
    {%-endif-%}
{% endmacro -%}

# macro for none var
{% macro var(var, data_input) -%}
{#-id 0: khong co list trong bieu thuc va condition -#}
{% if var['id'][0] == 0 -%}
    {#-with condititon-#}
    {%- if var['cond']|length > 0%}if {{var['cond']|safe}}:
        {{var['var']}} = {%if var['type'] == 'regex'%}{{var['val']|safe}}{%else-%}
                         {{var['type']}}({{var['val']|safe}}){%endif-%}
    {%- else -%}
    {#-without condition-#}
    {{var['var']}} = {%if var['type'] == 'regex'%}{{var['val']|safe}}{%else-%}
                     {{var['type']}}({{var['val']|safe}}){%endif-%}
    {%- endif -%}


{#-id 1: co list trong bieu thuc -#}
{%-elif var['id'][0] == 1 -%}

{#- 1 var list -#}
{%- if var['id'][1][1]|length == 1 -%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for x in {{var['id'][1][1][0]}}
    {#-with condititon-#}
    {%- if var['cond']|length > 0 %} if {{var['cond']|safe}}]
    {%-if var['type'] != 'regex'%}){%endif-%}
    {#-without condition-#}
    {%- else -%}]{%if var['type'] != 'regex'%}){%endif-%}
    {%- endif -%}

{#- 2 var list -#}
{%-elif var['id'][1][1]|length == 2-%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for (x_1, x_2) in zip({{var['id'][1][2][0]}}, {{var['id'][1][2][1]}})
    {#-with condititon-#}
    {%- if var['cond']|length > 0 %} if {{var['cond']|safe}}]
    {%-if var['type'] != 'regex'%}){%endif-%}
    {#-without condition-#}
    {%- else -%}]{%if var['type'] != 'regex'%}){%endif-%}
    {%- endif -%}

{#- 3 var list -#}
{%-elif var['id'][1][1]|length == 3-%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for (x_1, x_2, x_3) in zip({{var['id'][1][2][0]}}, {{var['id'][1][2][1]}}, {{var['id'][1][2][2]}})
    {#-with condititon-#}
    {%- if var['cond']|length > 0 %} if {{var['cond']|safe}}]
    {%-if var['type'] != 'regex'%}){%endif-%}
    {#-without condition-#}
    {%- else -%}]{%-if var['type'] != 'regex'%}){%endif-%}
    {%- endif -%}
{%- else -%}
    error
{%-endif-%}


{#-id 2: co list trong condition -#}
{%-elif var['id'][0] == 2 -%}
    {#- 1 var list -#}
    {%-if var['id'][1][0]|length == 1-%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for x in {{var['id'][1][2][0]}} if {{var['cond']|safe}}]
                     {%-if var['type'] != 'regex'%}){%endif-%}
    {#- 2 var list -#}  
    {%-elif var['id'][1][0]|length == 2-%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for (x_1, x_2) in zip({{var['id'][1][2][0]}}, {{var['id'][1][2][1]}}) if {{var['cond']|safe}}]
                     {%-if var['type'] != 'regex'%}){%endif-%}
    {#- 3 var list -#}  
    {%-elif var['id'][1][0]|length == 3-%} 
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for (x_1, x_2, x_3) in zip({{var['id'][1][2][0]}}, {{var['id'][1][2][1]}}, {{var['id'][1][2][2]}}) if {{var['cond']|safe}}]
                     {%-if var['type'] != 'regex'%}){%endif-%}
    {%- endif -%}


{#-id 3: co list trong condition -#}
{%-elif var['id'][0] == 3 -%}

    {#- 1 var list -#}
    {%-if var['id'][1][2]|length == 1-%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for x in {{var['id'][1][2][0]}} if {{var['cond']|safe}}]
                     {%-if var['type'] != 'regex'%}){%endif-%}

    {#- 2 var list -#}
    {%-elif var['id'][1][2]|length == 2-%}
    {{var['var']}} = {%if var['type'] != 'regex'-%}{{var['type']}}({%-endif-%}
                     [{{var['val']|safe}} for (x_1, x_2) in zip({{var['id'][1][2][0]}}, {{var['id'][1][2][1]}}) if {{var['cond']|safe}}]
                     {%-if var['type'] != 'regex'%}){%endif-%}

    {#- 3 var list -#}
    {%-elif var['id'][1][2]|length == 3-%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for (x_1, x_2, x_3) in zip({{var['id'][1][2][0]}}, {{var['id'][1][2][1]}}, {{var['id'][1][2][2]}}) if {{var['cond']|safe}}]
                        {%-if var['type'] != 'regex'%}){%endif-%}

    {#- 4 var list -#}
    {%-elif var['id'][1][2]|length == 4-%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for (x_1, x_2, x_3, x_4) in zip({{var['id'][1][2][0]}}, {{var['id'][1][2][1]}}, {{var['id'][1][2][2]}}, {{var['id'][1][2][3]}}) if {{var['cond']|safe}}]
                        {%-if var['type'] != 'regex'%}){%endif-%}

    {#- 5 var list -#}
    {%-elif var['id'][1][2]|length == 5-%}
    {{var['var']}} = {%if var['type'] != 'regex'%}{{var['type']}}({%endif-%}
                     [{{var['val']|safe}} for (x_1, x_2, x_3, x_4, x_5) in zip({{var['id'][1][2][0]}}, {{var['id'][1][2][1]}}, {{var['id'][1][2][2]}}, {{var['id'][1][2][3]}}, {{var['id'][1][2][4]}}) if {{var['cond']|safe}}]
                     {%-if var['type'] != 'regex'%}){%endif-%}
    {%- endif -%}

{%- endif -%}
{% endmacro -%}



