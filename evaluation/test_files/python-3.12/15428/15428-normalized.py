def items(self):
    """Get query with correct ordering."""
    if self.asc is not None:
        if self._selected and self.asc:
            return self.query.order_by(self._selected)
        elif self._selected and (not self.asc):
            return self.query.order_by(desc(self._selected))
    return self.query