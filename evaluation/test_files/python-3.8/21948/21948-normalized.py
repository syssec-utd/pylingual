def new_worksheet(name=None, cells=None):
    """Create a worksheet by name with with a list of cells."""
    ws = NotebookNode()
    if name is not None:
        ws.name = unicode(name)
    if cells is None:
        ws.cells = []
    else:
        ws.cells = list(cells)
    return ws