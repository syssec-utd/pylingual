def no_auto_store():
    """ Temporarily disable automatic registration of records in the auto_store

    Decorator factory. This is _NOT_ thread safe

    >>> @no_auto_store()
    ... class BarRecord(Record):
    ...     pass
    >>> BarRecord in auto_store
    False

    """
    original_auto_register_value = PySchema.auto_register
    disable_auto_register()

    def decorator(cls):
        PySchema.auto_register = original_auto_register_value
        return cls
    return decorator