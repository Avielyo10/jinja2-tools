"""
Lookup plugin
"""
import os
import sys

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
    else:
        raise ValueError(op)


def _resolve_file(lookup):
    """
    Implement file resolver
    """
    current_pwd = os.getcwd()
    if validate_is_file(os.path.join(current_pwd, lookup.arg)):
        with open(lookup.arg, 'r') as in_file:
            return in_file.read()


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
