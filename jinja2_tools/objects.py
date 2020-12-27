import json
import sys

from .exceptions import InvalidDataType
from .validators import validate_json
from .util import print_verbose, input_handler, load_yaml

from colors import red
from jinja2 import Template as Jinja2_template, exceptions


class Base:
    def __init__(self, data, verbose):
        self.data = data
        self.verbose = verbose


class ExtraVar(Base):
    def __init__(self, data, verbose):
        Base.__init__(self, data, verbose)
        self.data = dict(var.split('=') for var in self.data)
        for var in self.data:
            self.data[var] = validate_json(self.data[var])

    def get_extra_vars(self):
        print_verbose({'title': '[ExtraVars]', 'content': json.dumps(
            self.data, indent=2), 'verbose': self.verbose})
        return self.data


class Data(Base):
    def __init__(self, data, verbose):
        Base.__init__(self, data, verbose)

    def get_data(self):
        try:
            ih = input_handler(self.data)
        except InvalidDataType as err:
            print(err.message, file=sys.stderr)
            sys.exit(128)
        else:
            self.data = load_yaml(ih)
            print_verbose({'title': '[Data]', 'content': json.dumps(
                self.data, indent=2), 'verbose': self.verbose})
            return self.data


class Template(Base):
    def __init__(self, template, verbose, data, no_trim_blocks, no_lstrip_blocks):
        Base.__init__(self, data, verbose)
        self.template = template
        self.no_trim_blocks = no_trim_blocks
        self.no_lstrip_blocks = no_lstrip_blocks

    def __render(self):
        try:
            if self.data is not None:
                return self.template.render(self.data)
            else:
                return self.template.render()
        except exceptions.UndefinedError as err:
            print(red('[ERROR]'), err.message, file=sys.stderr)

    def get_rendered_template(self):
        try:
            ih = input_handler(self.template)
        except InvalidDataType as err:
            print(err.message, file=sys.stderr)
            sys.exit(128)
        else:
            print_verbose(
                {'title': '[Template]', 'content': ih, 'verbose': self.verbose})
            self.template = Jinja2_template(
                ih, trim_blocks=self.no_trim_blocks, lstrip_blocks=self.no_lstrip_blocks)
            return self.__render()
