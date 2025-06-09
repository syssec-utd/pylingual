def _get_exc_info(self, exc_tuple=None):
    """get exc_info from a given tuple, sys.exc_info() or sys.last_type etc.
        
        Ensures sys.last_type,value,traceback hold the exc_info we found,
        from whichever source.
        
        raises ValueError if none of these contain any information
        """
    if exc_tuple is None:
        etype, value, tb = sys.exc_info()
    else:
        etype, value, tb = exc_tuple
    if etype is None:
        if hasattr(sys, 'last_type'):
            etype, value, tb = (sys.last_type, sys.last_value, sys.last_traceback)
    if etype is None:
        raise ValueError('No exception to find')
    sys.last_type = etype
    sys.last_value = value
    sys.last_traceback = tb
    return (etype, value, tb)