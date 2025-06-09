def count_ops(self):
    """Count each operation kind in the circuit.

        Returns:
            dict: a breakdown of how many operations of each kind.
        """
    count_ops = {}
    for instr, _, _ in self.data:
        if instr.name in count_ops.keys():
            count_ops[instr.name] += 1
        else:
            count_ops[instr.name] = 1
    return count_ops