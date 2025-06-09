def _get_word_end_cursor(self, position):
    """ Find the end of the word to the right the given position. If a
            sequence of non-word characters precedes the first word, skip over
            them. (This emulates the behavior of bash, emacs, etc.)
        """
    document = self._control.document()
    end = self._get_end_cursor().position()
    while position < end and (not is_letter_or_number(document.characterAt(position))):
        position += 1
    while position < end and is_letter_or_number(document.characterAt(position)):
        position += 1
    cursor = self._control.textCursor()
    cursor.setPosition(position)
    return cursor