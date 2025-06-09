def _fetchChildren(self):
    """Fetch and return new child items."""
    children = []
    paths = []
    for name in os.listdir(self.path):
        paths.append(os.path.normpath(os.path.join(self.path, name)))
    collections, remainder = clique.assemble(paths, [clique.PATTERNS['frames']])
    for path in remainder:
        try:
            child = ItemFactory(path)
        except ValueError:
            pass
        else:
            children.append(child)
    for collection in collections:
        children.append(Collection(collection))
    return children