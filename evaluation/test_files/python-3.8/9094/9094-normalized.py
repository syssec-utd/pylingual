def _observe_block(self, change):
    """ A change handler for the 'objects' list of the Include.

        If the object is initialized objects which are removed will be
        unparented and objects which are added will be reparented. Old
        objects will be destroyed if the 'destroy_old' flag is True.

        """
    if self.is_initialized and change['type'] == 'update':
        old_block = change['oldvalue']
        for c in self.children:
            old_block.children.remove(c)
            c.set_parent(None)
        self.refresh_items()