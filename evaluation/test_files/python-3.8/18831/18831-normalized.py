def doAction(self, action):
    """
        Helper method that calls all callbacks registered for the given action.
        """
    if not hasattr(self, 'actions'):
        return
    for (f, args, kwargs) in self.actions.get(action, []):
        f(*args, **kwargs)