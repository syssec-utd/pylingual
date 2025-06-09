def validate(self, request):
    """Validate JSON-RPC request.

        :param request: RPC request object
        :type request: dict

        """
    try:
        validate_version(request)
        validate_method(request)
        validate_params(request)
        validate_id(request)
    except (AssertionError, KeyError) as error:
        invalid_request(error)