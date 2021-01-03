"""
Lookup plugin
"""
from io import StringIO
import os
import sys
import re
import configparser

from colors import red

from jinja2_tools.validators import validate_is_file


class Lookup:
    """
    Base class of lookup plugin
    """

    def __init__(self, args):
        if len(args) == 2:
            self.op, self.arg = args
        else:
            raise ValueError(args)


class LookupResolver:
    def resolve(_, lookup):
        """
        Get the right resolver and act accordingly
        """
        resolver = get_resolver(lookup.op)
        return resolver(lookup)


def get_resolver(op):
    """
    Get the right resolver
    """
    if op == 'env':
        return _resolve_env
    elif op == 'file':
        return _resolve_file
    elif op == 'ini':
        return _resolve_ini
    else:
        raise ValueError(op)


def handle_ini_args(ini_args):
    try:
        key = ini_args[0]  # The first value in the argument is the key
        ini_args = ini_args[1:]
    except ValueError:
        raise ValueError(ini_args)
    else:
        # Default args
        args = {
            'type': 'ini',
            'file': 'jinja.ini',
            'section': 'global',
            're': False,
            'default': ''
        }
        args['key'] = key
        args.update(dict(arg.split('=') for arg in ini_args))
        return args


def _resolve_ini(lookup):
    ini_args = handle_ini_args(lookup.arg.split(' '))
    config_parser = configparser.ConfigParser()
    file = ini_args['file']
    if not validate_is_file(file):
        raise ValueError(file)

    config = StringIO()
    if ini_args['type'] == 'properties':
        config.write('[java_properties]\n')
        ini_args['section'] = 'java_properties'

    with open(file, 'r') as ini_file:
        config.write(ini_file.read())
        config.seek(0, os.SEEK_SET)
    
    config_parser.read_file(config)
    if ini_args['re']:
        return [value for key, value in config_parser.items(ini_args['section']) if re.match(ini_args['key'], key)]
    return config_parser.get(ini_args['section'], ini_args['key'], fallback=ini_args['default'])


def _resolve_file(lookup):
    """
    Implement file resolver
    """
    current_pwd = os.getcwd()
    if validate_is_file(os.path.join(current_pwd, lookup.arg)):
        with open(lookup.arg, 'r') as in_file:
            return in_file.read()
    else:
        raise ValueError(f'{lookup.arg} is not a file.')


def _resolve_env(lookup):
    """
    Implement environment resolver
    """
    try:
        key = os.environ[lookup.arg]
    except OSError as err:
        print(red('[ERROR]'), err.strerror, file=sys.stderr)
    else:
        return key
