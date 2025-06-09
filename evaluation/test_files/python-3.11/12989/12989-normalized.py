def validate(validator):
    """
    Return a decorator that validates arguments with provided `validator`
    function.

    This will also store the validator function as `func.validate`.
    The decorator returned by this function, can bypass the validator
    if `validate=False` is passed as argument otherwise the fucntion is
    called directly.

    The validator must raise an exception, if the function can not
    be called.
    """

    def decorator(func):
        """Bound decorator to a particular validator function"""

        @wraps(func)
        def wrapper(image, size, validate=True):
            if validate:
                validator(image, size)
            return func(image, size)
        return wrapper
    return decorator