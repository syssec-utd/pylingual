def check_return(result, func, cargs):
    """Error checking for Error calls"""
    if result != 0:
        s = rt.Error_GetLastErrorMsg().decode()
        msg = 'LASError in "%s": %s' % (func.__name__, s)
        rt.Error_Reset()
        raise RTreeError(msg)
    return True