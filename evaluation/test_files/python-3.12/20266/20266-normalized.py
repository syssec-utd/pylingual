def _get_format_from_document(self, token, document):
    """ Returns a QTextCharFormat for token by
        """
    code, html = self._formatter._format_lines([(token, u'dummy')]).next()
    self._document.setHtml(html)
    return QtGui.QTextCursor(self._document).charFormat()