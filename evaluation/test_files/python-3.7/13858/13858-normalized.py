def insert(self, pos, values):
    """Insert a number of rows into the grid (and associated table)"""
    if isinstance(values, dict):
        row = GridRow(self, **values)
    else:
        row = GridRow(self, *values)
    list.insert(self, pos, row)
    self._grid_view.wx_obj.InsertRows(pos, numRows=1)