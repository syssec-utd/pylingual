def Rconverter(Robj, dataframe=False):
    """
    Convert an object in R's namespace to one suitable
    for ipython's namespace.

    For a data.frame, it tries to return a structured array.
    It first checks for colnames, then names.
    If all are NULL, it returns np.asarray(Robj), else
    it tries to construct a recarray

    Parameters
    ----------

    Robj: an R object returned from rpy2
    """
    is_data_frame = ro.r('is.data.frame')
    colnames = ro.r('colnames')
    rownames = ro.r('rownames')
    names = ro.r('names')
    if dataframe:
        as_data_frame = ro.r('as.data.frame')
        cols = colnames(Robj)
        _names = names(Robj)
        if cols != ri.NULL:
            Robj = as_data_frame(Robj)
            names = tuple(np.array(cols))
        elif _names != ri.NULL:
            names = tuple(np.array(_names))
        else:
            return np.asarray(Robj)
        Robj = np.rec.fromarrays(Robj, names=names)
    return np.asarray(Robj)