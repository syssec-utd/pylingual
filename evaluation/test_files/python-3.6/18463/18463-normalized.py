def intersection(self, sig: Scope) -> Scope:
    """ Create a new Set produce by the intersection of 2 Set """
    new = Scope(sig=self._hsig.values(), state=self.state)
    new &= sig
    return new