def request_token_handler(self, f):
    """Request token handler decorator.

        The decorated function should return an dictionary or None as
        the extra credentials for creating the token response.

        If you don't need to add any extra credentials, it could be as
        simple as::

            @app.route('/oauth/request_token')
            @oauth.request_token_handler
            def request_token():
                return {}
        """

    @wraps(f)
    def decorated(*args, **kwargs):
        server = self.server
        uri, http_method, body, headers = extract_params()
        credentials = f(*args, **kwargs)
        try:
            ret = server.create_request_token_response(uri, http_method, body, headers, credentials)
            return create_response(*ret)
        except errors.OAuth1Error as e:
            return _error_response(e)
    return decorated