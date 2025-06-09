def _onNavigate(self, index):
    """Handle selection of path segment."""
    if index > 0:
        self.setLocation(self._locationWidget.itemData(index), interactive=True)