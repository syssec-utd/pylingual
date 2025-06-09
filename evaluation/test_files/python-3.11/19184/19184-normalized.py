def odd_odd(self):
    """Selects odd-odd nuclei from the table:

        >>> Table('FRDM95').odd_odd
        Out[13]:
        Z   N
        9   9       1.21
            11      0.10
            13      3.08
            15      9.32
        ...
        """
    return self.select(lambda Z, N: Z % 2 and N % 2, name=self.name)