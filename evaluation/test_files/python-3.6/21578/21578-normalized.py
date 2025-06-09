def already_used(self, tok):
    """has this jwt been used?"""
    if tok in self.jwts:
        return True
    self.jwts[tok] = time.time()
    return False