def _create_value(self, *args, **kwargs):
    """
        Lowest value generator.

        Separated from __call__, because it seems that python
        cache __call__ reference on module import
        """
    if not len(args):
        raise TypeError('Object instance is not provided')
    if self.by_instance:
        field_type = args[0]
    else:
        field_type = args[0].__class__
    function = self.registry.get(field_type, self.default)
    if function is None:
        raise TypeError('no match %s' % field_type)
    return function(*args, **kwargs)