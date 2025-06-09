def comments(self):
    """The AST comments."""
    if self._comments is None:
        self._comments = [c for c in self.grammar.children if c.is_type(TokenType.comment)]
    return self._comments