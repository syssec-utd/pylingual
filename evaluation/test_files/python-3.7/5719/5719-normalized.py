def open(self):
    """initialize visit variables"""
    self.stats = self.linter.add_stats()
    self._returns = []
    self._branches = defaultdict(int)
    self._stmts = []