def _action__get(self):
    """
        Get/set the form's ``action`` attribute.
        """
    base_url = self.base_url
    action = self.get('action')
    if base_url and action is not None:
        return urljoin(base_url, action)
    else:
        return action