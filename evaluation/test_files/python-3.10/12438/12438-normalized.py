def with_open_store(func):
    """This is a decorator that signaling that a function is only available if the storage is open.

    """
    doc = func.__doc__
    na_string = '\nATTENTION: This function can only be used if the store is open!\n'
    if doc is not None:
        func.__doc__ = '\n'.join([doc, na_string])
    func._with_open_store = True

    @functools.wraps(func)
    def new_func(self, *args, **kwargs):
        if not self.traj.v_storage_service.is_open:
            raise TypeError('Function `%s` is only available if the storage is open.' % func.__name__)
        return func(self, *args, **kwargs)
    return new_func