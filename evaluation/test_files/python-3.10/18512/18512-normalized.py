def add_method(cls):
    """Attach a method to a class."""

    def wrapper(f):
        setattr(cls, f.__name__, f)
        return f
    return wrapper