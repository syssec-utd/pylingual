def init_app(self, app):
    """Initializes an app to work with this extension.

        The app-context signals will be subscribed and the template context
        will be initialized.

        :param app: the :class:`flask.Flask` app instance.
        """
    appcontext_pushed.connect(self.initialize_bars, app)
    app.add_template_global(self, 'nav')