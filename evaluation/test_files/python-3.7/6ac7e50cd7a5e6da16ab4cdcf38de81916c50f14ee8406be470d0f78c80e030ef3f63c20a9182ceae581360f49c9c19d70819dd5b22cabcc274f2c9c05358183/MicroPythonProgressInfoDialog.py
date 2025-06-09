"""
Module implementing a dialog to show progress messages.
"""
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QDialog
from .Ui_MicroPythonProgressInfoDialog import Ui_MicroPythonProgressInfoDialog

class MicroPythonProgressInfoDialog(QDialog, Ui_MicroPythonProgressInfoDialog):
    """
    Class implementing a dialog to show progress messages.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot(str)
    def addMessage(self, message):
        """
        Public slot to add a message to the progress display.

        @param message progress information to be shown
        @type str
        """
        tc = self.progressEdit.textCursor()
        tc.movePosition(QTextCursor.MoveOperation.End)
        self.progressEdit.setTextCursor(tc)
        self.progressEdit.appendHtml(message)
        self.progressEdit.ensureCursorVisible()