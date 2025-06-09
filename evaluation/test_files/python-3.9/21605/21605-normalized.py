def _clear_temporary_buffer(self):
    """ Clears the "temporary text" buffer, i.e. all the text following
            the prompt region.
        """
    cursor = self._get_prompt_cursor()
    prompt = self._continuation_prompt.lstrip()
    if self._temp_buffer_filled:
        self._temp_buffer_filled = False
        while cursor.movePosition(QtGui.QTextCursor.NextBlock):
            temp_cursor = QtGui.QTextCursor(cursor)
            temp_cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            text = temp_cursor.selection().toPlainText().lstrip()
            if not text.startswith(prompt):
                break
    else:
        return
    cursor.movePosition(QtGui.QTextCursor.Left)
    cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
    cursor.removeSelectedText()
    if self._control.isUndoRedoEnabled():
        self._control.setUndoRedoEnabled(False)
        self._control.setUndoRedoEnabled(True)