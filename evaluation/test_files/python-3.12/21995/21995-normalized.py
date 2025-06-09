def unreachable(self, completed, failed=None):
    """return whether this dependency has become impossible."""
    if len(self) == 0:
        return False
    against = set()
    if not self.success:
        against = completed
    if failed is not None and (not self.failure):
        against = against.union(failed)
    if self.all:
        return not self.isdisjoint(against)
    else:
        return self.issubset(against)