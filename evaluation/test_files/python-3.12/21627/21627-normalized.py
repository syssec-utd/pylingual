def _insert_plain_text(self, cursor, text):
    """ Inserts plain text using the specified cursor, processing ANSI codes
            if enabled.
        """
    cursor.beginEditBlock()
    if self.ansi_codes:
        for substring in self._ansi_processor.split_string(text):
            for act in self._ansi_processor.actions:
                if act.action == 'erase' and act.area == 'screen':
                    cursor.select(QtGui.QTextCursor.Document)
                    cursor.removeSelectedText()
                elif act.action == 'scroll' and act.unit == 'page':
                    cursor.insertText('\n')
                    cursor.endEditBlock()
                    self._set_top_cursor(cursor)
                    cursor.joinPreviousEditBlock()
                    cursor.deletePreviousChar()
                elif act.action == 'carriage-return':
                    cursor.movePosition(cursor.StartOfLine, cursor.KeepAnchor)
                elif act.action == 'beep':
                    QtGui.qApp.beep()
                elif act.action == 'backspace':
                    if not cursor.atBlockStart():
                        cursor.movePosition(cursor.PreviousCharacter, cursor.KeepAnchor)
                elif act.action == 'newline':
                    cursor.movePosition(cursor.EndOfLine)
            format = self._ansi_processor.get_format()
            selection = cursor.selectedText()
            if len(selection) == 0:
                cursor.insertText(substring, format)
            elif substring is not None:
                if len(substring) >= len(selection):
                    cursor.insertText(substring, format)
                else:
                    old_text = selection[len(substring):]
                    cursor.insertText(substring + old_text, format)
                    cursor.movePosition(cursor.PreviousCharacter, cursor.KeepAnchor, len(old_text))
    else:
        cursor.insertText(text)
    cursor.endEditBlock()