def _add_mode_t(s):
    """
O:O:.O:O:.-  => O:O:.O:O:.t.-
    """
    subst, attr, mode = s
    assert isinstance(mode, NullScript)
    return m(subst, attr, script('t.'))