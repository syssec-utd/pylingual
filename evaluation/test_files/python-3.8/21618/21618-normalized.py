def _get_input_buffer_cursor_line(self):
    """ Returns the text of the line of the input buffer that contains the
            cursor, or None if there is no such line.
        """
    prompt = self._get_input_buffer_cursor_prompt()
    if prompt is None:
        return None
    else:
        cursor = self._control.textCursor()
        text = self._get_block_plain_text(cursor.block())
        return text[len(prompt):]