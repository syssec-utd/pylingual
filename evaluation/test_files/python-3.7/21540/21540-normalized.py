def eventFilter(self, obj, event):
    """ Reimplemented to hide on certain key presses and on text edit focus
            changes.
        """
    if obj == self._text_edit:
        etype = event.type()
        if etype == QtCore.QEvent.KeyPress:
            key = event.key()
            if key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
                self.hide()
            elif key == QtCore.Qt.Key_Escape:
                self.hide()
                return True
        elif etype == QtCore.QEvent.FocusOut:
            self.hide()
        elif etype == QtCore.QEvent.Enter:
            self._hide_timer.stop()
        elif etype == QtCore.QEvent.Leave:
            self._leave_event_hide()
    return super(CallTipWidget, self).eventFilter(obj, event)