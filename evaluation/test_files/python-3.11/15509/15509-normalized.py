def icon(self, index):
    """Return icon for index."""
    sourceModel = self.sourceModel()
    if not sourceModel:
        return None
    return sourceModel.icon(self.mapToSource(index))