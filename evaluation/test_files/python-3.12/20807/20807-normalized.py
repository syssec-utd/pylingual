def show_items(self, cursor, items):
    """ Shows the completion widget with 'items' at the position specified
            by 'cursor'.
        """
    if not items:
        return
    self._start_position = cursor.position()
    self._consecutive_tab = 1
    items_m, ci = text.compute_item_matrix(items, empty=' ')
    self._sliding_interval = SlidingInterval(len(items_m) - 1)
    self._items = items_m
    self._size = (ci['rows_numbers'], ci['columns_numbers'])
    self._old_cursor = cursor
    self._index = (0, 0)
    sjoin = lambda x: [y.ljust(w, ' ') for y, w in zip(x, ci['columns_width'])]
    self._justified_items = map(sjoin, items_m)
    self._update_list(hilight=False)