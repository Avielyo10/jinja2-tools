import json
import os
import requests
import validators
import yaml
import sys

from .exceptions import InvalidDataType
from colors import red, green
from jinja2 import Template as Jinja2_template, exceptions


def print_verbose(message):
    if message['verbose']:
        separator = green(f'{"-" * 10}')
        print(separator, message['title'], separator)
        print(green(message['content']), "\n")


def load_yaml(data):
    return yaml.load(data, Loader=yaml.FullLoader)


def input_handler(data):
    if data == '-':
        return sys.stdin.read()
    elif validators.url(data):
        r = requests.get(data)
        if r.status_code < 400:
            return r.text
    elif os.path.exists(data):
        with open(data, 'r') as input_data_file:
            return input_data_file.read()
    else:
        raise InvalidDataType()


class Base:
    def __init__(self, data, verbose):
        self.data = data
        self.verbose = verbose


class Data(Base):
    def __init__(self, data, verbose):
        Base.__init__(self, data, verbose)

    def get_data(self):
        try:
            ih = input_handler(self.data)
        except InvalidDataType as err:
            print(err.message)
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
            print(red('[ERROR]'), err.message)

    def get_rendered_template(self):
        try:
            ih = input_handler(self.template)
        except InvalidDataType as err:
            print(err.message)
        else:
            print_verbose(
                {'title': '[Template]', 'content': ih, 'verbose': self.verbose})
            self.template = Jinja2_template(
                ih, trim_blocks=self.no_trim_blocks, lstrip_blocks=self.no_lstrip_blocks)
            return self.__render()
