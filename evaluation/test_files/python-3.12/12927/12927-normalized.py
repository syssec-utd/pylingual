def unapply_top_patch(self, force=False):
    """ Unapply top patch """
    self._check(force)
    patch = self.db.top_patch()
    self._unapply_patch(patch)
    self.db.save()
    self.unapplied(self.db.top_patch())