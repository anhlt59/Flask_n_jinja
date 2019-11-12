""" macro for load/save data
    func() class data has method check file, load, save
    load() init class data and create a object for load data
    save() save data
"""

# class
{% macro func(data_input) -%}
{% if data_input['list_last']|length > 0 -%}
class Data():
    """ Class for load/save data"""
    def __init__(self):
        self.dir_path = path.dirname(path.abspath(__file__))
        self.script_name = path.splitext(path.basename(__file__))[0]
        self.script_path = path.join(self.dir_path, self.script_name)
        {% if 'host' in data_input['option'] -%}
        self.filename = path.join(self.script_path, str(options.host) + ".tmp")
        {% else -%}
        self.filename = path.join(self.script_path, self.script_name + ".tmp")
        {% endif -%}
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
                return [{%for i in data_input['list_last']-%} None{%if loop.index < data_input['list_last']|length%}, {%endif%}
                       {%-endfor-%}]
{% endif %}
{% endmacro %}


# load data
    {% macro load(data_input) -%}
    {% if data_input['list_last']|length > 0 -%}
    # load data
    Data = Data()
    last_result = Data.load()
    {% endif %}
    {% endmacro -%}

# save data
    {% macro save(data_input) -%}
    {% if data_input['list_last']|length > 0 -%}
    # save data
    Data.save({% for i in data_input['list_last'] -%}{{i}}{%if loop.index < data_input['list_last']|length%}, {%endif%}{% endfor -%})
    {% endif %}
    {% endmacro -%}