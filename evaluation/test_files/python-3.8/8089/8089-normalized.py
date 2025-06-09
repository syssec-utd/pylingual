def delete(self, path):
    """
        Ensure that roots of our managers can't be deleted.  This should be
        enforced by https://github.com/ipython/ipython/pull/8168, but rogue
        implementations might override this behavior.
        """
    path = normalize_api_path(path)
    if path in self.managers:
        raise HTTPError(400, "Can't delete root of %s" % self.managers[path])
    return self.__delete(path)