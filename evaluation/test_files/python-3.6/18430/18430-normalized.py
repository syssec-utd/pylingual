def add_ignored(self, ignored):
    """Add ignored text to the node. This will add the length of the ignored text to the node's
    consumed property.
    """
    if ignored:
        if self.ignored:
            self.ignored = ignored + self.ignored
        else:
            self.ignored = ignored
    self.consumed += len(ignored)