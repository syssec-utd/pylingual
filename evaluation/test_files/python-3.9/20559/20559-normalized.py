def _type_pprint(obj, p, cycle):
    """The pprint for classes and types."""
    if obj.__module__ in ('__builtin__', 'exceptions'):
        name = obj.__name__
    else:
        name = obj.__module__ + '.' + obj.__name__
    p.text(name)