def _calc_c(self, a1, a2, r1, r2):
    """
        Compute the functions C1 and C2
        """
    if r1 == 0.0 and r2 == 0.0:
        return (a1, a2)
    div = 1 / (r1 + r2)
    c1 = (a1 * r2 + a2 * r1) * div
    c2 = (a1 * r1 + a2 * r2) * div
    return (c1, c2)