def check_valid(msg_type, attr, value, func, exec_info):
    """
    Checker function all validate_* functions below will call.
    Raises InvalidMessageInputError if input is not valid as per
    given func.
    """
    if value is not None:
        if isinstance(value, MutableSequence):
            for v in value:
                if not func(v):
                    raise InvalidMessageInputError(msg_type, attr, value, exec_info)
        elif not func(value):
            raise InvalidMessageInputError(msg_type, attr, value, exec_info)