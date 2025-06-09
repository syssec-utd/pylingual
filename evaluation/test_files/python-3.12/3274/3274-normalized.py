def str_rjust(x, width, fillchar=' '):
    """Fills the left side of string samples with a specified character such that the strings are left-hand justified.

    :param int width: The minimal width of the strings.
    :param str fillchar: The character used for filling.
    :returns: an expression containing the filled strings.

    Example:

    >>> import vaex
    >>> text = ['Something', 'very pretty', 'is coming', 'our', 'way.']
    >>> df = vaex.from_arrays(text=text)
    >>> df
      #  text
      0  Something
      1  very pretty
      2  is coming
      3  our
      4  way.

    >>> df.text.str.rjust(width=10, fillchar='!')
    Expression = str_rjust(text, width=10, fillchar='!')
    Length: 5 dtype: str (expression)
    ---------------------------------
    0   !Something
    1  very pretty
    2   !is coming
    3   !!!!!!!our
    4   !!!!!!way.
    """
    sl = _to_string_sequence(x).pad(width, fillchar, True, False)
    return column.ColumnStringArrow(sl.bytes, sl.indices, sl.length, sl.offset, string_sequence=sl)