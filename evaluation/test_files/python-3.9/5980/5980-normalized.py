def register_to(self, oauth, name=None, **kwargs):
    """Creates a remote app and registers it."""
    kwargs = self._process_kwargs(name=name or self.default_name, **kwargs)
    return oauth.remote_app(**kwargs)