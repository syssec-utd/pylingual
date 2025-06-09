def _set_base(self, default_base=None):
    """set the API base or default to use Docker Hub. The user is able
           to set the base, api version, and protocol via a settings file
           of environment variables:
 
           SREGISTRY_DOCKERHUB_BASE: defaults to index.docker.io
           SREGISTRY_DOCKERHUB_VERSION: defaults to v1
           SREGISTRY_DOCKERHUB_NO_HTTPS: defaults to not set (so https)

        """
    base = self._get_setting('SREGISTRY_DOCKERHUB_BASE')
    version = self._get_setting('SREGISTRY_DOCKERHUB_VERSION')
    if base is None:
        if default_base is None:
            base = 'index.docker.io'
        else:
            base = default_base
    if version is None:
        version = 'v2'
    nohttps = self._get_setting('SREGISTRY_DOCKERHUB_NOHTTPS')
    if nohttps is None:
        nohttps = 'https://'
    else:
        nohttps = 'http://'
    self._base = '%s%s' % (nohttps, base)
    self._version = version
    self.base = '%s%s/%s' % (nohttps, base.strip('/'), version)