def _isdupitem(self, key, val, dedup_result):
    """Return whether (key, val) duplicates an existing item."""
    isdupkey, isdupval, nodeinv, nodefwd = dedup_result
    isdupitem = nodeinv is nodefwd
    if isdupitem:
        assert isdupkey
        assert isdupval
    return isdupitem