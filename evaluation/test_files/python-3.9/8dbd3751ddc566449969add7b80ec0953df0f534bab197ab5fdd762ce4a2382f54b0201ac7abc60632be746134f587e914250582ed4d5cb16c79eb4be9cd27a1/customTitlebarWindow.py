from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QFont, QIcon
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout, QWidget, QMainWindow, QPushButton, QLabel, QMenuBar, QToolButton, QSizePolicy, QApplication
from pyqt_frameless_window.framelessWindow import FramelessWindow
from pyqt_top_titlebar_widget import TopTitleBarWidget
from pyqt_svg_label import SvgLabel
from pyqt_windows_buttons_widget import WindowsButtonsWidget
from pyqt_mac_buttons_widget import MacButtonsWidget

class CustomTitlebarWindow(FramelessWindow):

    def __init__(self, widget: QWidget):
        super().__init__(widget)
        self.__initVal(widget)
        self.__initUi()

    def __initVal(self, widget):
        self.__widget = widget
        self.__widget.setObjectName('mainWidget')
        self.__menubar = ''
        if isinstance(self.__widget, QMainWindow):
            self.__menubar = self.__widget.menuBar()
            self.__menubar.setObjectName('navWidget')
        self.__windowTitleIconLabel = QLabel()
        self.__titleLbl = QLabel()
        self.__iconLbl = QLabel()
        self.__topTitleBar = QWidget()
        self.__btnWidget = QWidget()
        self.__btnHint = ['min', 'max', 'close']
        self.__minimizeBtn = QPushButton()
        self.__maximizeBtn = QPushButton()
        self.__closeBtn = QPushButton()
        self.__style = QApplication.platformName()
        if self.__style == 'windows' or self.__style == 'mac':
            pass
        else:
            self.__style = 'windows'

    def __initUi(self):
        self.__widget.installEventFilter(self)
        self.installEventFilter(self)
        self.closeEvent = self.__widget.closeEvent
        lay = QGridLayout()
        lay.addWidget(self.__widget)
        lay.setContentsMargins(self._margin, self._margin, self._margin, self._margin)
        lay.setSpacing(self._margin)
        self.setLayout(lay)
        self.__modernizeAppFont()
        if isinstance(self.__menubar, QMenuBar):
            color = self.__menubar.palette().color(QPalette.Base)
            self.__initMenuBar()
        else:
            color = self.__widget.palette().color(QPalette.Base)
        self.setFrameColor(color)

    def __initMenuBar(self):
        self.__menubar.installEventFilter(self)
        tool_button = self.__menubar.findChild(QToolButton)
        tool_button.setArrowType(Qt.RightArrow)

    def __modernizeAppFont(self):
        appFont = QApplication.font()
        appFont.setFamily('Arial')
        appFont.setPointSize(min(12, max(9, appFont.pointSize() * QApplication.desktop().logicalDpiX() / 96.0)))
        appFont.setStyleStrategy(QFont.PreferAntialias)
        QApplication.setFont(appFont)
        QApplication.setEffectEnabled(Qt.UI_FadeMenu, True)
        QApplication.setEffectEnabled(Qt.UI_FadeTooltip, True)

    def eventFilter(self, obj, e) -> bool:
        if obj == self:
            if e.type() == 105:
                if int(e.oldState()) == 4:
                    if isinstance(self.__topTitleBar, TopTitleBarWidget):
                        self.__topTitleBar.show()
            elif e.type() == 17:
                menubarSizeHint = self.__menubar.sizeHint()
                widgetSizeHint = self.__widget.sizeHint()
                topTitleBarSizeHint = self.__topTitleBar.sizeHint() * 2
                min_width = max(menubarSizeHint.width(), widgetSizeHint.width(), topTitleBarSizeHint.width())
                min_height = max(menubarSizeHint.height(), widgetSizeHint.height(), topTitleBarSizeHint.height())
                self.setMinimumSize(min_width, min_height)
        if obj.objectName() == 'mainWidget':
            if e.type() == 19:
                self.close()
            if e.type() == 105:
                self.__toggleFullScreenFromInnerWidget(e)
            if e.type() == 33:
                title = obj.windowTitle()
                self.__titleLbl.setText(title)
                self.setWindowTitle(title)
        if e.type() == 10:
            self.unsetCursor()
            self._resizing = False
        if obj.objectName() == 'navWidget':
            if isinstance(obj, QMenuBar):
                if e.type() == 4 or e.type() == 5:
                    self.__execMenuBarMoveOrDoubleClickEvent(e)
                elif e.type() == 100:
                    cornerWidget = self.getCornerWidget()
                    if cornerWidget:
                        color = self.__menubar.palette().color(QPalette.Base)
                        cornerWidget.setStyleSheet(f'QWidget {{ background-color: {color.name()} }};')
                        self.__titleLbl.setStyleSheet(f'QWidget {{ background-color: {color.name()} }};')
            elif isinstance(obj, TopTitleBarWidget):
                if e.type() == 4 or e.type() == 5:
                    self.__execTitleBarMoveOrDoubleClickEvent(e)
        return super().eventFilter(obj, e)

    def __toggleFullScreenFromInnerWidget(self, e):
        inner_state = int(e.oldState())
        if inner_state == 0 or inner_state == 4:
            if inner_state == 0:
                if isinstance(self.__topTitleBar, TopTitleBarWidget):
                    self.__topTitleBar.hide()
                self.showFullScreen()
            else:
                if isinstance(self.__topTitleBar, TopTitleBarWidget):
                    self.__topTitleBar.show()
                self.showNormal()
            title_bar_state = self.windowState()
            self.__widget.setWindowState(title_bar_state)

    def __execMenuBarMoveOrDoubleClickEvent(self, e):
        p = e.pos()
        if self.__menubar.actionAt(p):
            pass
        elif self.__menubar.activeAction():
            pass
        elif e.type() == 4 and e.button() == Qt.LeftButton:
            self.__showNormalOrMaximized()
        else:
            self.setPressToMove(int(self.windowState()) != 4)
            if self.isPressToMove():
                self._move()

    def __execTitleBarMoveOrDoubleClickEvent(self, e):
        if e.type() == 4 and e.button() == Qt.LeftButton:
            self.__showNormalOrMaximized()
        else:
            self._move()

    def __showNormalOrMaximized(self):
        self.__execShowNormalOrMaximized()

    def __execShowNormalOrMaximized(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def setButtonHint(self, hint):
        self.__btnHint = hint

    def __getProperButtonsWidget(self, widget, btnWidget=None):
        if btnWidget:
            pass
        elif self.__style == 'windows':
            btnWidget = WindowsButtonsWidget(widget, self.__btnHint)
        elif self.__style == 'mac':
            btnWidget = MacButtonsWidget(widget, self.__btnHint)
        return btnWidget

    def setButtons(self, btnWidget=None, align=Qt.AlignRight):
        if isinstance(self.__topTitleBar, TopTitleBarWidget):
            self.__btnWidget = self.__getProperButtonsWidget(self.__topTitleBar, btnWidget)
            if isinstance(self.__btnWidget, WindowsButtonsWidget):
                align = Qt.AlignRight
            elif isinstance(self.__btnWidget, MacButtonsWidget):
                align = Qt.AlignLeft
            self.__topTitleBar.setButtons(self.__btnWidget, align)
            iconTitleWidget = self.__topTitleBar.getIconTitleWidget()
            self.initTitleEvent(iconTitleWidget)
            self.initButtonsEvent()
        else:
            lay = QHBoxLayout()
            lay.setContentsMargins(0, 0, 0, 0)
            self.__btnWidget = self.__getProperButtonsWidget(self.__menubar, btnWidget)
            self.initButtonsEvent()
            lay.addWidget(self.__btnWidget)
            w = h = self.__titleLbl.font().pointSize() * 3 * QApplication.screens()[0].logicalDotsPerInch() / 96.0
            self.__btnWidget.setButtonSize(w, h)
            cornerWidget = QWidget()
            cornerWidget.setLayout(lay)
            if self.__menubar:
                existingCornerWidget = self.__menubar.cornerWidget(Qt.TopRightCorner)
                if existingCornerWidget:
                    lay.insertWidget(0, existingCornerWidget)
                    if self.__titleLbl.text():
                        lay.insertWidget(0, self.__titleLbl)
                cornerWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
                cornerWidget.setMinimumHeight(self.__menubar.height())
                self.__menubar.setCornerWidget(cornerWidget, Qt.TopRightCorner)

    def __getWindowTitle(self, title):
        if title:
            pass
        else:
            title = self.__widget.windowTitle()
        return title

    def __getWindowIcon(self, icon_filename):
        if icon_filename:
            pass
        else:
            icon_filename = self.__widget.windowIcon().name()
        return icon_filename

    def __setWindowIcon(self, icon_filename):
        icon_filename = self.__getWindowIcon(icon_filename)
        self.setWindowIcon(QIcon(icon_filename))

    def __setMenuTitle(self, title, font):
        self.__titleLbl.setText(title)
        self.__titleLbl.setFont(font)
        self.__titleLbl.setMinimumHeight(self.__menubar.height())
        cornerWidget = self.__menubar.cornerWidget()
        if cornerWidget:
            lay = cornerWidget.layout()
            if lay:
                lay.insertWidget(0, self.__titleLbl)
        else:
            self.__menubar.setCornerWidget(self.__titleLbl, Qt.TopRightCorner)

    def __setMenuIcon(self, icon_filename):
        self.__iconLbl = SvgLabel()
        self.__iconLbl.setSvgFile(icon_filename)
        w = h = self.__titleLbl.font().pointSize() * 2 * QApplication.screens()[0].logicalDotsPerInch() / 96.0
        self.__iconLbl.setFixedSize(w, h)
        lay = QHBoxLayout()
        lay.addWidget(self.__iconLbl)
        lay.setContentsMargins(5, 0, 0, 0)
        leftCornerWidget = QWidget()
        leftCornerWidget.setLayout(lay)
        self.__menubar.setCornerWidget(leftCornerWidget, Qt.TopLeftCorner)

    def setMenuAsTitleBar(self, title: str='', icon_filename: str='', font: QFont=QFont('Arial', 9)):
        title = self.__getWindowTitle(title)
        self.setWindowTitle(title)
        self.__setWindowIcon(icon_filename)
        self.__setMenuTitle(title, font)
        self.__setMenuIcon(icon_filename)

    def setTopTitleBar(self, title: str='', icon_filename: str='', font: QFont=QFont('Arial', 14), align=Qt.AlignCenter, bottom_separator: bool=False):
        title = self.__getWindowTitle(title)
        self.setWindowTitle(title)
        self.__setWindowIcon(icon_filename)
        if isinstance(self.__menubar, QMenuBar):
            self.__topTitleBar = TopTitleBarWidget(self.__menubar, text=title, font=font, icon_filename=icon_filename, align=align)
            self.__menubar.removeEventFilter(self)
        else:
            self.__topTitleBar = TopTitleBarWidget(self.__widget, text=title, font=font, icon_filename=icon_filename, align=align)
        self.__topTitleBar.installEventFilter(self)
        self.__topTitleBar.setObjectName('navWidget')
        if bottom_separator:
            self.__topTitleBar.setBottomSeparator()
        lay = self.layout()
        centralWidget = lay.itemAt(0).widget()
        lay.addWidget(self.__topTitleBar, 0, 0, 1, 1)
        lay.addWidget(centralWidget, 1, 0, 1, 1)
        self.setPressToMove(False)

    def getCornerWidget(self):
        return self.__menubar.cornerWidget()

    def initTitleEvent(self, titleWidget):
        self.__windowTitleIconLabel = titleWidget.getSvgLabel()
        self.__titleLbl = titleWidget.getTextLabel()

    def initButtonsEvent(self):
        self.__minimizeBtn = self.__btnWidget.getMinimizedBtn()
        self.__maximizeBtn = self.__btnWidget.getMaximizedBtn()
        self.__closeBtn = self.__btnWidget.getCloseBtn()
        self.__fixBtn = self.__btnWidget.getFixBtn()
        self.__minimizeBtn.clicked.connect(self.showMinimized)
        self.__maximizeBtn.clicked.connect(self.__showNormalOrMaximized)
        self.__closeBtn.clicked.connect(self.close)
        self.__fixBtn.clicked.connect(self.fix)

    def fix(self, f):
        if f:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def getInnerWidget(self):
        return self.__widget