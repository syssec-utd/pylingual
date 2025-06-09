def get_font(family, fallback=None):
    """Return a font of the requested family, using fallback as alternative.

    If a fallback is provided, it is used in case the requested family isn't
    found.  If no fallback is given, no alternative is chosen and Qt's internal
    algorithms may automatically choose a fallback font.

    Parameters
    ----------
    family : str
      A font name.
    fallback : str
      A font name.

    Returns
    -------
    font : QFont object
    """
    font = QtGui.QFont(family)
    font_info = QtGui.QFontInfo(font)
    if fallback is not None and font_info.family() != family:
        font = QtGui.QFont(fallback)
    return font