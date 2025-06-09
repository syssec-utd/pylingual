def read_las(source, closefd=True):
    """ Entry point for reading las data in pylas

    Reads the whole file into memory.

    >>> las = read_las("pylastests/simple.las")
    >>> las.classification
    array([1, 1, 1, ..., 1, 1, 1], dtype=uint8)

    Parameters
    ----------
    source : str or io.BytesIO
        The source to read data from

    closefd: bool
            if True and the source is a stream, the function will close it
            after it is done reading


    Returns
    -------
    pylas.lasdatas.base.LasBase
        The object you can interact with to get access to the LAS points & VLRs
    """
    with open_las(source, closefd=closefd) as reader:
        return reader.read()