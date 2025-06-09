def handle_url_build_error(self, error, endpoint, values):
    """Handle :class:`~werkzeug.routing.BuildError` on :meth:`url_for`.
        """
    (exc_type, exc_value, tb) = sys.exc_info()
    for handler in self.url_build_error_handlers:
        try:
            rv = handler(error, endpoint, values)
            if rv is not None:
                return rv
        except BuildError as error:
            pass
    if error is exc_value:
        reraise(exc_type, exc_value, tb)
    raise error