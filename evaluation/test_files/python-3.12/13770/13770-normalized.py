def auth_get_token(self, check_scope=True):
    """Refresh or acquire access_token."""
    res = self.auth_access_data_raw = self._auth_token_request()
    return self._auth_token_process(res, check_scope=check_scope)