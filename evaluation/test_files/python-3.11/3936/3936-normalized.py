def q_if(self, *qregs):
    """Add controls to all instructions."""
    for gate in self.instructions:
        gate.q_if(*qregs)
    return self