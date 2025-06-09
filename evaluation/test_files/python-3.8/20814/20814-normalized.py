def validate_pin(pin):
    """ Validate the given pin against the schema.

    :param dict pin: The pin to validate:
    :raises pypebbleapi.schemas.DocumentError: If the pin is not valid.
    """
    v = _Validator(schemas.pin)
    if v.validate(pin):
        return
    else:
        raise schemas.DocumentError(errors=v.errors)