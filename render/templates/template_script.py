#!/usr/bin/python
# -*- coding: utf-8 -*-
{%- block library -%}
{% endblock %}

{% block function %}{% endblock %}

if __name__ == '__main__':
    # Exit statuses recognized by Nagios
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    {% block input %}{% endblock -%}

    {% block variable %}{% endblock -%}

    {% block condition %}{% endblock -%}