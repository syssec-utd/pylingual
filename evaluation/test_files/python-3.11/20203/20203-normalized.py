def show_items(self, cursor, items):
    """ Shows the completion widget with 'items' at the position specified
            by 'cursor'.
        """
    text_edit = self._text_edit
    point = text_edit.cursorRect(cursor).bottomRight()
    point = text_edit.mapToGlobal(point)
    height = self.sizeHint().height()
    screen_rect = QtGui.QApplication.desktop().availableGeometry(self)
    if screen_rect.size().height() - point.y() - height < 0:
        point = text_edit.mapToGlobal(text_edit.cursorRect().topRight())
        point.setY(point.y() - height)
    self.move(point)
    self._start_position = cursor.position()
    self.clear()
    self.addItems(items)
    self.setCurrentRow(0)
    self.show()