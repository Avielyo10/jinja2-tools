"""
Data objects
"""
import json
import sys

from colors import red
from jinja2 import Template as Jinja2_template, exceptions

from .exceptions import InvalidDataType
from .plugins import plugins
from .util import print_verbose, input_handler, load_yaml
from .validators import validate_json


class Base:
    """
    Simple base class that fits it all
    """

    def __init__(self, data, verbose):
        self.data = data
        self.verbose = verbose


class ExtraVar(Base):
    """
    ExtraVar can give you the ability to specify data without
    creating any file, this can be great for debugging or overwriting
    some variables in the data file.
    """

    def __init__(self, data, verbose):
        Base.__init__(self, data, verbose)
        self.data = dict(var.split('=') for var in self.data)
        for var in self.data:
            self.data[var] = validate_json(self.data[var])

    def get_extra_vars(self):
        """
        A simple getter with verbose option
        """
        print_verbose({'title': '[ExtraVars]', 'content': json.dumps(
            self.data, indent=2), 'verbose': self.verbose})
        return self.data


class Data(Base):
    """
    A class that holds the data
    """

    def __init__(self, data, verbose):
        Base.__init__(self, data, verbose)

    def get_data(self):
        """
        Decide how to interpret the data & load it in a way that the
        Template class can render.
        For now it can load both YAMLs & JSONs.
        """
        try:
            ih_content = input_handler(self.data)
        except InvalidDataType as err:
            print(err.message, file=sys.stderr)
            sys.exit(128)
        else:
            self.data = load_yaml(ih_content)
            print_verbose({'title': '[Data]', 'content': json.dumps(
                self.data, indent=2), 'verbose': self.verbose})
            return self.data


class Template(Base):
    """
    Used to render the template using the data
    """

    def __init__(self, template, verbose, data, options):
        Base.__init__(self, data, verbose)
        self.template = template
        self.no_trim_blocks = options['no_trim_blocks']
        self.no_lstrip_blocks = options['no_lstrip_blocks']

    def __render(self):
        """
        Decide whether to render with data or not.
        There is an option to render using only extra variables.
        """
        try:
            self.data.update(plugins())
            return self.template.render(self.data)
        except exceptions.UndefinedError as err:
            print(red('[ERROR]'), err.message, file=sys.stderr)

    def get_rendered_template(self):
        """
        Decide how to interpret the template, and return its rendered version.
        """
        try:
            ih_content = input_handler(self.template)
        except InvalidDataType as err:
            print(err.message, file=sys.stderr)
            sys.exit(128)
        else:
            print_verbose(
                {'title': '[Template]', 'content': ih_content, 'verbose': self.verbose})
            self.template = Jinja2_template(
                ih_content,
                trim_blocks=self.no_trim_blocks,
                lstrip_blocks=self.no_lstrip_blocks,
            )
            return self.__render()
