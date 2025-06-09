def f_delete_item(self, item, *args, **kwargs):
    """Deletes a single item, see :func:`~pypet.trajectory.Trajectory.f_delete_items`"""
    self.f_delete_items([item], *args, **kwargs)