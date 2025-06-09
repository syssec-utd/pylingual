def _handle_non_existant_index(cls):
    """
        Handle and check that some configuration index exists.
        """
    try:
        PyFunceble.INTERN['http_code']
    except KeyError:
        PyFunceble.INTERN['http_code'] = '*' * 3
    try:
        PyFunceble.INTERN['referer']
    except KeyError:
        PyFunceble.INTERN['referer'] = 'Unknown'