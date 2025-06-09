def _find_statements(self):
    """Find the statements in `self.code`.

        Produce a sequence of line numbers that start statements.  Recurses
        into all code objects reachable from `self.code`.

        """
    for bp in self.child_parsers():
        for (_, l) in bp._bytes_lines():
            yield l