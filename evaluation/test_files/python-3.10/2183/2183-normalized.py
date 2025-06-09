def deprecated(message):
    """The decorator to mark deprecated functions."""
    from traceback import extract_stack
    assert message, '`message` argument in @deprecated is required.'

    def deprecated_decorator(fun):

        def decorator_invisible(*args, **kwargs):
            stack = extract_stack()
            assert len(stack) >= 2 and stack[-1][2] == 'decorator_invisible', 'Got confusing stack... %r' % stack
            print('[WARNING] in %s line %d:' % (stack[-2][0], stack[-2][1]))
            print('    >>> %s' % (stack[-2][3] or '????'))
            print('        ^^^^ %s' % message)
            return fun(*args, **kwargs)
        decorator_invisible.__doc__ = message
        decorator_invisible.__name__ = fun.__name__
        decorator_invisible.__module__ = fun.__module__
        decorator_invisible.__deprecated__ = True
        return decorator_invisible
    return deprecated_decorator