import os
import requests
import yaml
import sys

from .validators import validate_url, validate_is_file
from .exceptions import InvalidDataType

from colors import green


def print_verbose(message):
    if message['verbose']:
        separator = green(f'{"-" * 10}')
        print(separator, message['title'], separator)
        print(green(message['content']), "\n")


def load_yaml(data):
    return yaml.load(data, Loader=yaml.FullLoader)


def output_template(content, output_path, dir=None):
    if content is not None:
        if output_path is None:
            print(content)
        else:
            if dir is not None:
                dir = output_path + dir
                if dir is not os.path.exists(os.path.dirname(dir)):
                    os.makedirs(os.path.dirname(dir), exist_ok=True)
                output_path = dir
            with open(output_path, 'w+') as output_file:
                output_file.write(content)


def input_handler(data):
    if data == '-':
        return sys.stdin.read()
    elif validate_url(data):
        r = requests.get(data)
        if not r.raise_for_status():
            return r.text
    elif validate_is_file(data):
        with open(data, 'r') as input_data_file:
            return input_data_file.read()
    else:
        raise InvalidDataType()
