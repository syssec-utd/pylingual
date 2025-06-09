def current_scope(self):
    """ node.Base: The current node relative to which all interaction will be scoped. """
    scope = self._scopes[-1]
    if scope in [None, 'frame']:
        scope = self.document
    return scope