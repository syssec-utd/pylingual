def draw(self, cr, highlight=False, bounding=None):
    """Draw this shape with the given cairo context"""
    if bounding is None or self._intersects(bounding):
        self._draw(cr, highlight, bounding)