def directives(self):
    """The diretives parsed from the comments."""
    if self._directives is None:
        self._directives = []
        for comment in self.comments:
            self._directives.extend(self.directives_from_comment(comment))
    return self._directives