def _check_compatible_regs(self, rhs):
    """Raise exception if the circuits are defined on incompatible registers"""
    list1 = self.qregs + self.cregs
    list2 = rhs.qregs + rhs.cregs
    for element1 in list1:
        for element2 in list2:
            if element2.name == element1.name:
                if element1 != element2:
                    raise QiskitError('circuits are not compatible')