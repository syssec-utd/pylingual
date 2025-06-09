def get_trim_index(biased_list):
    """Returns the trim index from a ``bool`` list

    Provided with a list of ``bool`` elements (``[False, False, True, True]``),
    this function will assess the index of the list that minimizes the number
    of True elements (biased positions) at the extremities. To do so,
    it will iterate over the boolean list and find an index position where
    there are two consecutive ``False`` elements after a ``True`` element. This
    will be considered as an optimal trim position. For example, in the
    following list::

        [True, True, False, True, True, False, False, False, False, ...]

    The optimal trim index will be the 4th position, since it is the first
    occurrence of a ``True`` element with two False elements after it.

    If the provided ``bool`` list has no ``True`` elements, then the 0 index is
    returned.

    Parameters
    ----------
    biased_list: list
        List of ``bool`` elements, where ``True`` means a biased site.

    Returns
    -------
        x : index position of the biased list for the optimal trim.

    """
    if set(biased_list) == {False}:
        return 0
    if set(biased_list[:5]) == {False}:
        return 0
    for i, val in enumerate(biased_list):
        if val and set(biased_list[i + 1:i + 3]) == {False}:
            return i + 1
    return len(biased_list)