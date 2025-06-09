def c_if(self, classical, val):
    """Add classical control register to all instructions."""
    for gate in self.instructions:
        gate.c_if(classical, val)
    return self