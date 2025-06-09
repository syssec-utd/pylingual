def asAMP(cls):
    """
        Returns the exception's name in an AMP Command friendly format.

        For example, given a class named ``ExampleExceptionClass``, returns
        ``"EXAMPLE_EXCEPTION_CLASS"``.
        """
    parts = groupByUpperCase(cls.__name__)
    return (cls, '_'.join((part.upper() for part in parts)))