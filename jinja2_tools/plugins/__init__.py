from .lookup import Lookup, LookupResolver


def lookup(*args):
    lookup_resolver = LookupResolver()
    lookup = Lookup(args)
    return lookup_resolver.resolve(lookup)


def plugins():
    plugins = {
        'lookup': lookup
    }
    return plugins
