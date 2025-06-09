from PyQt6 import QtCore, QtGui, QtWidgets
from gotify_tray.database import Settings
from gotify_tray.utils import get_abs_path
settings = Settings('gotify-tray')

class StatusWidget(QtWidgets.QLabel):

    def __init__(self):
        super(StatusWidget, self).__init__()
        self.setFixedSize(QtCore.QSize(20, 20))
        self.setScaledContents(True)
        self.set_connecting()

    def set_status(self, image: str):
        self.setPixmap(QtGui.QPixmap(get_abs_path(f'gotify_tray/gui/images/{image}')))

    def set_active(self):
        self.setToolTip('Listening for new messages')
        self.set_status('status_active.svg')

    def set_connecting(self):
        self.setToolTip('Connecting...')
        self.set_status('status_connecting.svg')

    def set_inactive(self):
        self.setToolTip('Listener inactive')
        self.set_status('status_inactive.svg')

    def set_error(self):
        self.setToolTip('Listener error')
        self.set_status('status_error.svg')