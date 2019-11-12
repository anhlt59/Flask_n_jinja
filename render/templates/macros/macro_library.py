# macro for library

{%- macro func(data_input) -%}
{%- for i in data_input['library'] -%}
{{i}}
{% endfor -%}
{% endmacro -%}