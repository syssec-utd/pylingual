def authorized_handler(self, f):
    """Handles an OAuth callback.

        .. versionchanged:: 0.7
           @authorized_handler is deprecated in favor of authorized_response.
        """

    @wraps(f)
    def decorated(*args, **kwargs):
        log.warn('@authorized_handler is deprecated in favor of authorized_response')
        data = self.authorized_response()
        return f(*(data,) + args, **kwargs)
    return decorated