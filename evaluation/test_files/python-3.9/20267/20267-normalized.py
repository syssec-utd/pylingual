def _get_format_from_style(self, token, style):
    """ Returns a QTextCharFormat for token by reading a Pygments style.
        """
    result = QtGui.QTextCharFormat()
    for (key, value) in style.style_for_token(token).items():
        if value:
            if key == 'color':
                result.setForeground(self._get_brush(value))
            elif key == 'bgcolor':
                result.setBackground(self._get_brush(value))
            elif key == 'bold':
                result.setFontWeight(QtGui.QFont.Bold)
            elif key == 'italic':
                result.setFontItalic(True)
            elif key == 'underline':
                result.setUnderlineStyle(QtGui.QTextCharFormat.SingleUnderline)
            elif key == 'sans':
                result.setFontStyleHint(QtGui.QFont.SansSerif)
            elif key == 'roman':
                result.setFontStyleHint(QtGui.QFont.Times)
            elif key == 'mono':
                result.setFontStyleHint(QtGui.QFont.TypeWriter)
    return result