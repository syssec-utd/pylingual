def accumulator(init, update):
    """
    Generic accumulator function.

    .. code-block:: python

        # Simplest Form
        >>> a = 'this' + ' '
        >>> b = 'that'
        >>> c = functools.reduce(accumulator, a, b)
        >>> c
        'this that'

        # The type of the initial value determines output type.
        >>> a = 5
        >>> b = Hello
        >>> c = functools.reduce(accumulator, a, b)
        >>> c
        10

    :param init:  Initial Value
    :param update: Value to accumulate

    :return: Combined Values
    """
    return init + len(update) if isinstance(init, int) else init + update