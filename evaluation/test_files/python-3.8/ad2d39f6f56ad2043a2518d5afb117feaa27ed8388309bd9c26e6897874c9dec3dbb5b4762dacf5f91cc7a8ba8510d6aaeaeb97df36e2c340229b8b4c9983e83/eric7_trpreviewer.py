"""
eric TR Previewer.

This is the main Python script that performs the necessary initialization
of the tr previewer and starts the Qt event loop. This is a standalone version
of the integrated tr previewer.
"""
import os
import sys
from PyQt6.QtGui import QGuiApplication
for arg in sys.argv[:]:
    if arg.startswith('--config='):
        from eric7 import Globals
        configDir = arg.replace('--config=', '')
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith('--settings='):
        from PyQt6.QtCore import QSettings
        settingsDir = os.path.expanduser(arg.replace('--settings=', ''))
        if not os.path.isdir(settingsDir):
            os.makedirs(settingsDir)
        QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, settingsDir)
        sys.argv.remove(arg)
from eric7.EricWidgets.EricApplication import EricApplication
from eric7.Globals import AppInfo
from eric7.Toolbox import Startup
from eric7.Tools.TRSingleApplication import TRSingleApplicationClient
app = None

def createMainWidget(argv):
    """
    Function to create the main widget.

    @param argv list of commandline parameters (list of strings)
    @return reference to the main widget (QWidget)
    """
    from eric7.Tools.TRPreviewer import TRPreviewer
    files = argv[1:] if len(argv) > 1 else []
    previewer = TRPreviewer(files, None, 'TRPreviewer')
    return previewer

def main():
    """
    Main entry point into the application.
    """
    global app
    QGuiApplication.setDesktopFileName('eric7_trpreviewer.desktop')
    options = [('--config=configDir', 'use the given directory as the one containing the config files'), ('--settings=settingsDir', 'use the given directory to store the settings files')]
    appinfo = AppInfo.makeAppInfo(sys.argv, 'eric TR Previewer', 'file', 'TR file previewer', options)
    Startup.setLibraryPaths()
    app = EricApplication(sys.argv)
    client = TRSingleApplicationClient()
    res = client.connect()
    if res > 0:
        if len(sys.argv) > 1:
            client.processArgs(sys.argv[1:])
        sys.exit(0)
    elif res < 0:
        print('eric7_trpreviewer: {0}'.format(client.errstr()))
        sys.exit(res)
    else:
        res = Startup.simpleAppStartup(sys.argv, appinfo, createMainWidget, app=app)
        sys.exit(res)
if __name__ == '__main__':
    main()