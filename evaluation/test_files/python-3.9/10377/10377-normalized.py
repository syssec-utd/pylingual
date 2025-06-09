def _rotate_sc_additive(s):
    """
    s.-S:.U:.-'l.-S:.O:.-'n.-S:.U:.-',+M:.-'M:.-'n.-S:.U:.-',  =>
    n.-S:.U:.-'s.-S:.U:.-'l.-S:.O:.-',+n.-S:.U:.-‘M:.-‘M:.-‘,"""
    if isinstance(s, AdditiveScript):
        return AdditiveScript([_rotate_sc(_s) for _s in s])
    else:
        return _rotate_sc(s)