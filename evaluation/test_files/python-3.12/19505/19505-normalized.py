def create(self, tarball_url, env=None, app_name=None):
    """Creates a Heroku app-setup build.

        :param tarball_url: URL of a tarball containing an ``app.json``.
        :param env: (optional) Dict containing environment variable overrides.
        :param app_name: (optional) Name of the Heroku app to create.
        :returns: A tuple with ``(build_id, app_name)``.
        """
    data = self._api.create_build(tarball_url=tarball_url, env=env, app_name=app_name)
    return (data['id'], data['app']['name'])