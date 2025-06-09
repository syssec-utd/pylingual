def logger(function):
    """Decorate passed in function and log message to module logger."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        """Wrap function."""
        sep = kwargs.get('sep', ' ')
        end = kwargs.get('end', '')
        out = sep.join([repr(x) for x in args])
        out = out + end
        _LOGGER.debug(out)
        return function(*args, **kwargs)
    return wrapper