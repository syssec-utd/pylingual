def sort(coll, f=None) -> Optional[ISeq]:
    """Return a sorted sequence of the elements in coll. If a comparator
    function f is provided, compare elements in coll using f."""
    return to_seq(sorted(coll, key=Maybe(f).map(functools.cmp_to_key).value))