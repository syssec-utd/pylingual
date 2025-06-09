def require_setting(self, name, feature='this feature'):
    """Raises an exception if the given app setting is not defined."""
    if name not in self.settings:
        raise Exception("You must define the '%s' setting in your application to use %s" % (name, feature))