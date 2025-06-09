def exhaust(fn, transform=None, *args, **kwargs):
    """
        Repeatedly call a function, starting with init, until false-y, yielding each item in turn.

        The ``transform`` parameter can be used to map a collection to another format, for example iterating over a
        :class:`dict` by value rather than key.

        Use with state-synced functions to retrieve all results.

        Args:
            fn (method): function to call
            transform (method): secondary function to convert result into an iterable
            args (list): positional arguments to pass to ``fn``
            kwargs (dict): keyword arguments to pass to ``fn``

        Returns:
            generator: generator of objects produced from the method
        """
    while True:
        iterRes = fn(*args, **kwargs)
        if iterRes:
            for item in transform(iterRes) if transform else iterRes:
                yield item
        else:
            break