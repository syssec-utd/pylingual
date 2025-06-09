def add_remote_app(self, remote_app, name=None, **kwargs):
    """Adds remote application and applies custom attributes on it.

        If the application instance's name is different from the argument
        provided name, or the keyword arguments is not empty, then the
        application instance will not be modified but be copied as a
        prototype.

        :param remote_app: the remote application instance.
        :type remote_app: the subclasses of :class:`BaseApplication`
        :params kwargs: the overriding attributes for the application instance.
        """
    if name is None:
        name = remote_app.name
    if name != remote_app.name or kwargs:
        remote_app = copy.copy(remote_app)
        remote_app.name = name
        vars(remote_app).update(kwargs)
    if not hasattr(remote_app, 'clients'):
        remote_app.clients = cached_clients
    self.remote_apps[name] = remote_app
    return remote_app