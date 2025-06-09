def _update_secrets(self):
    """update secrets will take a secrets credential file
        either located at .sregistry or the environment variable
        SREGISTRY_CLIENT_SECRETS and update the current client 
        secrets as well as the associated API base.
        """
    self.secrets = read_client_secrets()
    if self.secrets is not None:
        if 'registry' in self.secrets:
            if 'base' in self.secrets['registry']:
                self.base = self.secrets['registry']['base']
                self._update_base()