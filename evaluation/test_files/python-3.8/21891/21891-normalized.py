def with_objattrs(*names):
    """
    like `with_objattr` but enter context one by one.
    """

    def _wrap(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            with contextlib.ExitStack() as stack:
                for name in names:
                    stack.enter_context(getattr(self, name))
                return func(self, *args, **kwargs)
        return wrapper
    return _wrap