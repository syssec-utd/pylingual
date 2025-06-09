def record(self, func):
    """Registers a function that is called when the blueprint is
        registered on the application.  This function is called with the
        state as argument as returned by the :meth:`make_setup_state`
        method.
        """
    if self._got_registered_once and self.warn_on_modifications:
        from warnings import warn
        warn(Warning('The blueprint was already registered once but is getting modified now.  These changes will not show up.'))
    self.deferred_functions.append(func)