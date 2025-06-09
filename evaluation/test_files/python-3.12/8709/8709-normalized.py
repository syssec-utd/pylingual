def _compare_uids(uid1, uid2):
    """Calculate the minimum length of initial substrings of uid1 and uid2
        for them to be different.

        :param uid1: first uid to compare
        :type uid1: str
        :param uid2: second uid to compare
        :type uid2: str
        :returns: the length of the shortes unequal initial substrings
        :rtype: int
        """
    sum = 0
    for char1, char2 in zip(uid1, uid2):
        if char1 == char2:
            sum += 1
        else:
            break
    return sum