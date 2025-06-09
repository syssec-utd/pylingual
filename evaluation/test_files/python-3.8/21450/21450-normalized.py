def _context_menu_make(self, pos):
    """ Reimplemented to add an action for raw copy.
        """
    menu = super(FrontendWidget, self)._context_menu_make(pos)
    for before_action in menu.actions():
        if before_action.shortcut().matches(QtGui.QKeySequence.Paste) == QtGui.QKeySequence.ExactMatch:
            menu.insertAction(before_action, self._copy_raw_action)
            break
    return menu