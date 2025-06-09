def init_app(self, app):
    """
        Initializes the Flask-Allows object against the provided application
        """
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    app.extensions['allows'] = self

    @app.before_request
    def start_context(*a, **k):
        self.overrides.push(Override())
        self.additional.push(Additional())

    @app.after_request
    def cleanup(response):
        self.clear_all_overrides()
        self.clear_all_additional()
        return response