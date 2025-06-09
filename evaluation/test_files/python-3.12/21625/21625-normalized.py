def _insert_html(self, cursor, html):
    """ Inserts HTML using the specified cursor in such a way that future
            formatting is unaffected.
        """
    cursor.beginEditBlock()
    cursor.insertHtml(html)
    cursor.movePosition(QtGui.QTextCursor.Left, QtGui.QTextCursor.KeepAnchor)
    if cursor.selection().toPlainText() == ' ':
        cursor.removeSelectedText()
    else:
        cursor.movePosition(QtGui.QTextCursor.Right)
    cursor.insertText(' ', QtGui.QTextCharFormat())
    cursor.endEditBlock()