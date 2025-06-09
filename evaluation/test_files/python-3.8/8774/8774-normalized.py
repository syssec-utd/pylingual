def commit(self, full=False, all=False, force=False):
    """
        Call ``.save()`` on all modified entities in the session. Also forgets
        all known entities in the session, so this should only be called at
        the end of a request.

        Arguments:

            * *full* - pass ``True`` to force save full entities, not only
              changes
            * *all* - pass ``True`` to save all entities known, not only those
              entities that have been modified.
            * *full* - pass ``True`` to force-save all entities known, ignoring
              DataRaceError and EntityDeletedError exceptions
        """
    changes = self.flush(full, all, force)
    self.known = {}
    return changes