def _edges_changed(self, object, name, undefined, event):
    """ Handles addition and removal of edges.
        """
    self._delete_edges(event.removed)
    self._add_edges(event.added)