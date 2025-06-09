def show_tip(self, tip):
    """ Attempts to show the specified tip at the current cursor location.
        """
    text_edit = self._text_edit
    document = text_edit.document()
    cursor = text_edit.textCursor()
    search_pos = cursor.position() - 1
    (self._start_position, _) = self._find_parenthesis(search_pos, forward=False)
    if self._start_position == -1:
        return False
    self.setText(tip)
    self.resize(self.sizeHint())
    padding = 3
    cursor_rect = text_edit.cursorRect(cursor)
    screen_rect = QtGui.qApp.desktop().screenGeometry(text_edit)
    point = text_edit.mapToGlobal(cursor_rect.bottomRight())
    point.setY(point.y() + padding)
    tip_height = self.size().height()
    tip_width = self.size().width()
    vertical = 'bottom'
    horizontal = 'Right'
    if point.y() + tip_height > screen_rect.height():
        point_ = text_edit.mapToGlobal(cursor_rect.topRight())
        if point_.y() - tip_height < padding:
            if 2 * point.y() < screen_rect.height():
                vertical = 'bottom'
            else:
                vertical = 'top'
        else:
            vertical = 'top'
    if point.x() + tip_width > screen_rect.width():
        point_ = text_edit.mapToGlobal(cursor_rect.topRight())
        if point_.x() - tip_width < padding:
            if 2 * point.x() < screen_rect.width():
                horizontal = 'Right'
            else:
                horizontal = 'Left'
        else:
            horizontal = 'Left'
    pos = getattr(cursor_rect, '%s%s' % (vertical, horizontal))
    point = text_edit.mapToGlobal(pos())
    if vertical == 'top':
        point.setY(point.y() - tip_height - padding)
    if horizontal == 'Left':
        point.setX(point.x() - tip_width - padding)
    self.move(point)
    self.show()
    return True