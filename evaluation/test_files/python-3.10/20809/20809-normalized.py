def _complete_current(self):
    """ Perform the completion with the currently selected item.
        """
    i = self._index
    item = self._items[i[0]][i[1]]
    item = item.strip()
    if item:
        self._current_text_cursor().insertText(item)
    self.cancel_completion()