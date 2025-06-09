def update_setting(self, name, value):
    """Just update a setting, doesn't need to be returned.
    """
    if value is not None:
        updates = {name: value}
        update_client_secrets(backend=self.client_name, updates=updates)