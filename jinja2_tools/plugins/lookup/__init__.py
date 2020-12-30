import os
import sys

from colors import red


class Lookup:
    def __init__(self, args):
      if len(args) == 2:
        self.op, self.args = args
      else:
        raise ValueError(args)


class LookupResolver:
    def resolve(self, lookup):
        if lookup.op == 'env':
            try:
                key = os.environ[lookup.args]
            except OSError as err:
                print(red('[ERROR]'), err.strerror, file=sys.stderr)
            else:
                return key
        else:
            raise ValueError(lookup.op)
