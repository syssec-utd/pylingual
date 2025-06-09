def _get_stm_with_branches(stm_it):
    """
    :return: first statement with rank > 0 or None if iterator empty
    """
    last = None
    while last is None or last.rank == 0:
        try:
            last = next(stm_it)
        except StopIteration:
            last = None
            break
    return last