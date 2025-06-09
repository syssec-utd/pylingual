def _bits_in_condition(self, cond):
    """Return a list of bits in the given condition.

        Args:
            cond (tuple or None): optional condition (ClassicalRegister, int)

        Returns:
            list[(ClassicalRegister, idx)]: list of bits
        """
    all_bits = []
    if cond is not None:
        all_bits.extend([(cond[0], j) for j in range(self.cregs[cond[0].name].size)])
    return all_bits