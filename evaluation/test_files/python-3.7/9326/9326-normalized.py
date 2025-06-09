def refresh(self, force=False, soon=86400):
    """
        Refreshes the credentials only if the **provider** supports it and if
        it will expire in less than one day. It does nothing in other cases.

        .. note::

            The credentials will be refreshed only if it gives sense
            i.e. only |oauth2|_ has the notion of credentials
            *refreshment/extension*.
            And there are also differences across providers e.g. Google
            supports refreshment only if there is a ``refresh_token`` in
            the credentials and that in turn is present only if the
            ``access_type`` parameter was set to ``offline`` in the
            **user authorization request**.

        :param bool force:
            If ``True`` the credentials will be refreshed even if they
            won't expire soon.

        :param int soon:
            Number of seconds specifying what means *soon*.

        """
    if hasattr(self.provider_class, 'refresh_credentials'):
        if force or self.expire_soon(soon):
            logging.info('PROVIDER NAME: {0}'.format(self.provider_name))
            return self.provider_class(self, None, self.provider_name).refresh_credentials(self)