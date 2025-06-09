def _get_end_cursor(self):
    """ Convenience method that returns a cursor for the last character.
        """
    cursor = self._control.textCursor()
    cursor.movePosition(QtGui.QTextCursor.End)
    return cursor