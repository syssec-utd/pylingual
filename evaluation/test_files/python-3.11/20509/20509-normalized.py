def arcs_unpredicted(self):
    """Returns a sorted list of the executed arcs missing from the code."""
    possible = self.arc_possibilities()
    executed = self.arcs_executed()
    unpredicted = [e for e in executed if e not in possible and e[0] != e[1]]
    return sorted(unpredicted)