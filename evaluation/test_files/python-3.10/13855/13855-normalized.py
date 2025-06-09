def _updateColAttrs(self, grid):
    """update the column attributes to add the appropriate renderer"""
    col = 0
    for column in self.columns:
        attr = gridlib.GridCellAttr()
        if False:
            attr.SetReadOnly()
        if False:
            attr.SetRenderer(renderer)
        grid.SetColSize(col, column.width)
        grid.SetColAttr(col, attr)
        col += 1