def get_value(self, key):
    """
        Fetch the settings value with the highest precedence for the given
         key, or raise KeyError.
        Precedence:
          - IDB scope
          - directory scope
          - user scope
          - system scope

        type key: basestring
        rtype value: Union[basestring, int, float, List, Dict]
        """
    try:
        return self.idb.get_value(key)
    except (KeyError, EnvironmentError):
        pass
    try:
        return self.directory.get_value(key)
    except (KeyError, EnvironmentError):
        pass
    try:
        return self.user.get_value(key)
    except KeyError:
        pass
    try:
        return self.system.get_value(key)
    except KeyError:
        pass
    raise KeyError('key not found')