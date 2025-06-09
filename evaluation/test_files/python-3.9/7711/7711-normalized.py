def thickest(self, n=1, index=False):
    """
        Returns the thickest interval(s) as a striplog.

        Args:
            n (int): The number of thickest intervals to return. Default: 1.
            index (bool): If True, only the indices of the intervals are
                returned. You can use this to index into the striplog.

        Returns:
            Interval. The thickest interval. Or, if ``index`` was ``True``,
            the index of the thickest interval.
        """
    s = sorted(range(len(self)), key=lambda k: self[k].thickness)
    indices = s[-n:]
    if index:
        return indices
    elif n == 1:
        i = indices[0]
        return self[i]
    else:
        return self[indices]