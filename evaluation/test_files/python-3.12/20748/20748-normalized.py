def extract_vars_above(*names):
    """Extract a set of variables by name from another frame.

    Similar to extractVars(), but with a specified depth of 1, so that names
    are exctracted exactly from above the caller.

    This is simply a convenience function so that the very common case (for us)
    of skipping exactly 1 frame doesn't have to construct a special dict for
    keyword passing."""
    callerNS = sys._getframe(2).f_locals
    return dict(((k, callerNS[k]) for k in names))