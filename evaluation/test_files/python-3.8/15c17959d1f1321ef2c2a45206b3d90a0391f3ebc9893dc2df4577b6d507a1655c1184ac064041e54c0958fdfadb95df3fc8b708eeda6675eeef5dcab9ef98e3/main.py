import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon
from cracker.cracker import Cracker

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Cracker')
    cracker = Cracker(app)
    cracker.run()
    icon = QIcon('icon.png')
    tray = QSystemTrayIcon(icon)
    tray.setIcon(icon)
    tray.setVisible(True)
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()