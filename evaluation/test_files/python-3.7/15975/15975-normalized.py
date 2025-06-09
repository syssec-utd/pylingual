def is_invalid_marker(cls, text):
    """
        Validate text as a PEP 426 environment marker; return an exception
        if invalid or False otherwise.
        """
    try:
        cls.evaluate_marker(text)
    except SyntaxError as e:
        return cls.normalize_exception(e)
    return False