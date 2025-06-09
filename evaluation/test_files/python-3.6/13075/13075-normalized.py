def check_required(obj, required_parameters):
    """
    Check if a parameter is available on an object

    :param obj: Object
    :param required_parameters: list of parameters
    :return:
    """
    for parameter in required_parameters:
        if not hasattr(obj, parameter) or getattr(obj, parameter) is None:
            raise DesignError("parameter '%s' must be set for '%s' object." % (parameter, obj.base_type))