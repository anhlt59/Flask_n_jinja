# !/usr/bin/python
# library
# if linux using killpg instead kill
from os import kill, path, rmdir, remove
from jinja2 import Environment, FileSystemLoader, select_autoescape
from subprocess import Popen, PIPE, TimeoutExpired
from signal import SIGINT
import re

# from config import ROOT_PATH, SCRIPT_PATH, TEMPLATE_PATH, FORM_DATA, TEST
from handler import modify


class Script:
    """Class Render."""

    def __init__(self, config data_input):
        self.config = config
        self.data_input = modify(data_input, config.FORM_DATA)
        self.name = data_input.get('name', 'UNKNOWN')
        # self.check_err()
        # environment jinja
        self.path = config.ROOT_PATH
        self.env = Environment(
            loader=FileSystemLoader(config.TEMPLATE_PATH),
            autoescape=select_autoescape(['py'])
        )

    def check_err(self):
        """Check error."""
        if len(self.data_input['err']) > 0:
            raise Exception("Can't render script\n" +
                            str(self.data_input['err']))

    def render(self):
        """Render Script."""
        template = self.env.get_template('script_check_snmp.py')
        script = template.render(data_input=self.data_input)
        # fix too many blank line
        script = re.sub(
            r'(\s*\n\s*\n\s*\n\s*\n)|(\s*\n\s*\n\s*\n)|(\s*\n\s*\n)',
            lambda x: '\n\n', script)
        script = re.sub(r'\n\s*(?=output\()', lambda x: '\n    ', script)
        script = re.sub(r'(?<=status,\smessage\))\n\n', lambda x: '\n', script)

        with open(path.join(SCRIPT_PATH, self.name + '.py'), 'w') as file:
            file.write(script)

    def run(name, command):
        """Run script."""
        args = ['python2', path.join(self.config.SCRIPT_PATH, name + '.py')]
        args.extend(command.split(' '))
        # linux add attribute preexec_fn=setsid
        with Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
            try:
                stdout, stderr = proc.communicate(timeout=2)
            except TimeoutExpired:
                kill(proc.pid, SIGINT)
                return 'Timeout Expired!'
        return stdout.decode() if len(stderr) == 0 else stderr.decode()

    def delete(name):
        """Delete Script."""
        try:
            remove(path.join(self.config.SCRIPT_PATH, name + ".py"))
            rmdir(path.join(self.config.SCRIPT_PATH, name))
        except:
            pass
        return "SUCCESS"


if __name__ == '__main__':
    Script(TEST).render()
