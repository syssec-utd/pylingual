def lookup_signum(name):
    """Find the corresponding signal number for 'name'. Return None
    if 'name' is invalid."""
    uname = name.upper()
    if uname.startswith('SIG') and hasattr(signal, uname):
        return getattr(signal, uname)
    else:
        uname = 'SIG' + uname
        if hasattr(signal, uname):
            return getattr(signal, uname)
        return None
    return