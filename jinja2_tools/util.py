"""
Utility
"""
import os
import sys
import requests
import yaml

from colors import green

from .validators import validate_url, validate_is_file
from .exceptions import InvalidDataType


def print_verbose(message):
    """Print verbose output to stdout"""
    if message['verbose']:
        separator = green(f'{"-" * 10}')
        print(separator, message['title'], separator)
        print(green(message['content']), "\n")


def load_yaml(data):
    """Load YAML / JSON"""
    return yaml.load(data, Loader=yaml.FullLoader)


def output_template(content, output_path, dir=None):
    """Print template to stdout by default
    If output_path is not None, write the template content
    to the path that was specified.
    If dir is not None, copy the template directory with all
    templates applied.
    """
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
    """Handle & validate input"""
    ih_content = None
    if data == '-':
        ih_content = sys.stdin.read()
    elif validate_url(data):
        response = requests.get(data)
        if not response.raise_for_status():
            ih_content = response.text
    elif validate_is_file(data):
        with open(data, 'r') as input_data_file:
            ih_content = input_data_file.read()
    else:
        raise InvalidDataType()
    return ih_content
