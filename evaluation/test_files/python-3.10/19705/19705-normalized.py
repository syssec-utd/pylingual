def tokens_required(service_list):
    """
    Ensure the user has the necessary tokens for the specified services
    """

    def decorator(func):

        @wraps(func)
        def inner(request, *args, **kwargs):
            for service in service_list:
                if service not in request.session['user_tokens']:
                    return redirect('denied')
            return func(request, *args, **kwargs)
        return inner
    return decorator