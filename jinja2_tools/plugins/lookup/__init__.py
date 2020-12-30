"""
Lookup plugin
"""
import os
import sys

from colors import red


class Lookup:
    """
    Base class of lookup plugin
    """
    def __init__(self, args):
        if len(args) == 2:
            self.op, self.args = args
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
    else:
        raise ValueError(op)


def _resolve_env(lookup):
    """
    Implement environment resolver
    """
    try:
        key = os.environ[lookup.args]
    except OSError as err:
        print(red('[ERROR]'), err.strerror, file=sys.stderr)
    else:
        return key
