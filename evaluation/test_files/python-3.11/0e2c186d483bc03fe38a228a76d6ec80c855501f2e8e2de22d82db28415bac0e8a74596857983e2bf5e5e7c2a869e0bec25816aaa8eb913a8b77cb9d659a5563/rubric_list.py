import html
import logging
from textwrap import shorten
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPalette, QCursor
from PyQt5.QtWidgets import QAbstractItemView, QAction, QCheckBox, QLabel, QComboBox, QDialog, QDialogButtonBox, QInputDialog, QFormLayout, QGridLayout, QHBoxLayout, QMenu, QMessageBox, QPushButton, QToolButton, QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget, QTabBar, QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget
from plom.misc_utils import next_in_longest_subsequence
from .useful_classes import WarnMsg, SimpleQuestion
from .rubric_wrangler import RubricWrangler
log = logging.getLogger('annotr')
abs_suffix = ' / N'
abs_suffix_length = len(abs_suffix)

def isLegalRubric(mss, kind, delta):
    """Checks the 'legality' of the current rubric - returning one of three possible states
    0 = incompatible - the kind of rubric is not compatible with the current state
    1 = compatible but out of range - the kind of rubric is compatible with the state but applying that rubric will take the score out of range [0, maxmark] (so cannot be used)
    2 = compatible and in range - is compatible and can be used.
    Note that the rubric lists use the result to decide which rubrics will be shown (return value 2) which hidden (0 return) and greyed out (1 return)


    Args:
        mss (list): triple that encodes max-mark, state, and current-score
        kind: the kind of the rubric being checked
        delta: the delta of the rubric being checked

    Returns:
        int: 0,1,2.
    """
    maxMark = mss[0]
    state = mss[1]
    score = mss[2]
    if state == 'neutral' or kind == 'neutral':
        return 2
    if state == 'absolute' or kind == 'absolute':
        return 0
    idelta = int(delta)
    if state == 'up':
        if idelta < 0:
            return 0
        elif idelta + score > maxMark:
            return 1
        else:
            return 2
    elif idelta > 0:
        return 0
    elif idelta + score < 0:
        return 1
    else:
        return 2

class RubricTable(QTableWidget):

    def __init__(self, parent, shortname=None, sort=False, tabType=None):
        super().__init__(parent)
        self._parent = parent
        self.tabType = tabType
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)
        self.setGridStyle(Qt.DotLine)
        self.setAlternatingRowColors(False)
        self.setStyleSheet('\n            QHeaderView::section {\n                background-color: palette(window);\n                color: palette(dark);\n                padding-left: 1px;\n                padding-right: -3px;\n                border: none;\n            }\n            QTableView {\n                border: none;\n            }\n        ')
        f = self.font()
        f.setPointSizeF(0.67 * f.pointSizeF())
        self.verticalHeader().setFont(f)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['Key', 'Username', 'Delta', 'Text', 'Kind'])
        self.hideColumn(0)
        self.hideColumn(1)
        self.hideColumn(4)
        if self.tabType == 'delta':
            self.hideColumn(3)
        if sort:
            self.setSortingEnabled(True)
        self.shortname = shortname
        self.pressed.connect(self.handleClick)
        self.doubleClicked.connect(self.editRow)

    def set_name(self, newname):
        log.debug('tab %s changing name to %s', self.shortname, newname)
        self.shortname = newname
        self._parent.update_tab_names()

    def is_user_tab(self):
        return self.tabType is None

    def is_delta_tab(self):
        return self.tabType == 'delta'

    def is_hidden_tab(self):
        return self.tabType == 'hide'

    def is_shared_tab(self):
        return self.tabType == 'show'

    def contextMenuEvent(self, event):
        if self.is_hidden_tab():
            self.hideContextMenuEvent(event)
        elif self.is_shared_tab():
            self.showContextMenuEvent(event)
        elif self.is_user_tab():
            self.defaultContextMenuEvent(event)
        elif self.is_delta_tab():
            self.tabContextMenuEvent(event)
        else:
            event.ignore()

    def tabContextMenuEvent(self, event):
        menu = QMenu(self)
        a = QAction('Add new tab', self)
        a.triggered.connect(lambda: self._parent.add_new_tab())
        menu.addAction(a)
        menu.popup(QCursor.pos())
        event.accept()

    def defaultContextMenuEvent(self, event):
        row = self.rowAt(event.pos().y())
        if row < 0:
            row = self.getCurrentRubricRow()
        key = None if row is None else self.getKeyFromRow(row)

        def add_func_factory(t, k):

            def add_func():
                t.appendByKey(k)
            return add_func

        def del_func_factory(t, k):

            def del_func():
                t.removeRubricByKey(k)
            return del_func

        def edit_func_factory(t, k):

            def edit_func():
                t._parent.edit_rubric(k)
            return edit_func
        menu = QMenu(self)
        if key:
            a = QAction('Edit rubric', self)
            a.triggered.connect(edit_func_factory(self, key))
            menu.addAction(a)
            menu.addSeparator()
            for tab in self._parent.user_tabs:
                if tab == self:
                    continue
                a = QAction(f'Move to tab {tab.shortname}', self)
                a.triggered.connect(add_func_factory(tab, key))
                a.triggered.connect(del_func_factory(self, key))
                menu.addAction(a)
            menu.addSeparator()
            remAction = QAction('Remove from this tab', self)
            remAction.triggered.connect(del_func_factory(self, key))
            menu.addAction(remAction)
            menu.addSeparator()
        a = QAction('Rename this tab...', self)
        a.triggered.connect(self._parent.rename_current_tab)
        menu.addAction(a)
        a = QAction('Add new tab', self)
        a.triggered.connect(self._parent.add_new_tab)
        menu.addAction(a)
        a = QAction('Remove this tab...', self)
        a.triggered.connect(self._parent.remove_current_tab)
        menu.addAction(a)
        menu.popup(QCursor.pos())
        event.accept()

    def showContextMenuEvent(self, event):
        row = self.rowAt(event.pos().y())
        if row < 0:
            row = self.getCurrentRubricRow()
        key = None if row is None else self.getKeyFromRow(row)

        def add_func_factory(t, k):

            def add_func():
                t.appendByKey(k)
            return add_func

        def edit_func_factory(t, k):

            def edit_func():
                t._parent.edit_rubric(k)
            return edit_func
        menu = QMenu(self)
        if key:
            a = QAction('Edit rubric', self)
            a.triggered.connect(edit_func_factory(self, key))
            menu.addAction(a)
            menu.addSeparator()
            for tab in self._parent.user_tabs:
                a = QAction(f'Add to tab {tab.shortname}', self)
                a.triggered.connect(add_func_factory(tab, key))
                menu.addAction(a)
            menu.addSeparator()
            hideAction = QAction('Hide rubric', self)
            hideAction.triggered.connect(self.hideCurrentRubric)
            menu.addAction(hideAction)
            menu.addSeparator()
        a = QAction('Rename this tab...', self)
        a.triggered.connect(self._parent.rename_current_tab)
        menu.addAction(a)
        a = QAction('Add new tab', self)
        a.triggered.connect(self._parent.add_new_tab)
        menu.addAction(a)
        menu.popup(QCursor.pos())
        event.accept()

    def hideContextMenuEvent(self, event):
        menu = QMenu(self)
        unhideAction = QAction('Unhide rubric', self)
        unhideAction.triggered.connect(self.unhideCurrentRubric)
        menu.addAction(unhideAction)
        menu.popup(QCursor.pos())
        event.accept()

    def removeCurrentRubric(self):
        row = self.getCurrentRubricRow()
        if row is None:
            return
        self.removeRow(row)
        self.selectRubricByVisibleRow(0)
        self.handleClick()

    def removeRubricByKey(self, key):
        row = self.getRowFromKey(key)
        if row is None:
            return
        self.removeRow(row)
        self.selectRubricByVisibleRow(0)
        self.handleClick()

    def hideCurrentRubric(self):
        row = self.getCurrentRubricRow()
        if row is None:
            return
        key = self.item(row, 0).text()
        self._parent.hideRubricByKey(key)
        self.removeRow(row)
        self.selectRubricByVisibleRow(0)
        self.handleClick()

    def unhideCurrentRubric(self):
        row = self.getCurrentRubricRow()
        if row is None:
            return
        key = self.item(row, 0).text()
        self._parent.unhideRubricByKey(key)
        self.removeRow(row)
        self.selectRubricByVisibleRow(0)
        self.handleClick()

    def dropEvent(self, event):
        if event.source() == self:
            event.setDropAction(Qt.CopyAction)
            sourceRow = self.selectedIndexes()[0].row()
            targetRow = self.indexAt(event.pos()).row()
            if targetRow == -1:
                targetRow = self.rowCount()
            self.insertRow(targetRow)
            if targetRow < sourceRow:
                sourceRow += 1
            for col in range(0, self.columnCount()):
                self.setItem(targetRow, col, self.takeItem(sourceRow, col))
            self.selectRow(targetRow)
            self.removeRow(sourceRow)
            event.accept()

    def appendByKey(self, key):
        """Append the rubric associated with a key to the end of the list

        If its a dupe, don't add.

        args
            key (str/int?): the key associated with a rubric.

        raises
            what happens on invalid key?
        """
        rubric, = [x for x in self._parent.rubrics if x['id'] == key]
        self.appendNewRubric(rubric)

    def appendNewRubric(self, rubric):
        rc = self.rowCount()
        for r in range(rc):
            if rubric['id'] == self.item(r, 0).text():
                return
        self.insertRow(rc)
        self.setItem(rc, 0, QTableWidgetItem(rubric['id']))
        self.setItem(rc, 1, QTableWidgetItem(rubric['username']))
        if rubric['kind'] == 'absolute':
            self.setItem(rc, 2, QTableWidgetItem(rubric['delta'] + abs_suffix))
        else:
            self.setItem(rc, 2, QTableWidgetItem(rubric['delta']))
        self.setItem(rc, 3, QTableWidgetItem(rubric['text']))
        self.setItem(rc, 4, QTableWidgetItem(rubric['kind']))
        self.setVerticalHeaderItem(rc, QTableWidgetItem('{}'.format(rc + 1)))
        self.colourLegalRubric(rc, self._parent.mss)
        self.item(rc, 2).setToolTip('{}-rubric'.format(rubric['kind']))
        hoverText = ''
        if rubric['tags'] != '':
            hoverText += 'Tagged as {}\n'.format(rubric['tags'])
        if rubric['meta'] != '':
            hoverText += '{}\n'.format(rubric['meta'])
        self.item(rc, 3).setToolTip(hoverText.strip())

    def setRubricsByKeys(self, rubric_list, key_list):
        """Clear table and repopulate rubrics in the key_list"""
        for r in range(self.rowCount()):
            self.removeRow(0)
        rkl = [X['id'] for X in rubric_list]
        for id in key_list:
            try:
                rb = rubric_list[rkl.index(id)]
            except (ValueError, KeyError, IndexError):
                continue
            self.appendNewRubric(rb)
        self.resizeColumnsToContents()

    def setDeltaRubrics(self, rubrics, positive=True):
        """Clear table and repopulate with delta-rubrics"""
        for r in range(self.rowCount()):
            self.removeRow(0)
        delta_rubrics = []
        for rb in rubrics:
            if rb['username'] == 'manager' and rb['kind'] == 'delta':
                if positive and int(rb['delta']) > 0 or (not positive and int(rb['delta']) < 0):
                    delta_rubrics.append(rb)
        for rb in sorted(delta_rubrics, key=lambda r: abs(int(r['delta']))):
            self.appendNewRubric(rb)
        for rb in rubrics:
            if rb['username'] == 'manager' and rb['kind'] == 'absolute':
                self.appendNewRubric(rb)

    def getKeyFromRow(self, row):
        return self.item(row, 0).text()

    def getKeyList(self):
        return [self.item(r, 0).text() for r in range(self.rowCount())]

    def getRowFromKey(self, key):
        for r in range(self.rowCount()):
            if int(self.item(r, 0).text()) == int(key):
                return r
        else:
            return None

    def getCurrentRubricRow(self):
        if not self.selectedIndexes():
            return None
        return self.selectedIndexes()[0].row()

    def getCurrentRubricKey(self):
        if not self.selectedIndexes():
            return None
        return self.item(self.selectedIndexes()[0].row(), 0).text()

    def reselectCurrentRubric(self):
        r = self.getCurrentRubricRow()
        if r is None:
            if self.rowCount() == 0:
                return
            else:
                r = 0
        self.selectRubricByVisibleRow(r)

    def selectRubricByRow(self, r):
        """Select the r'th rubric in the list

        Args:
            r (int): The row-number in the rubric-table.
            If r is None, do nothing.
        """
        if r is not None:
            self.selectRow(r)

    def selectRubricByVisibleRow(self, r):
        """Select the r'th **visible** row

        Args:
            r (int): The row-number in the rubric-table.
            If r is None, do nothing.
        """
        rc = -1
        for s in range(self.rowCount()):
            if not self.isRowHidden(s):
                rc += 1
            if rc == r:
                self.selectRow(s)
                return
        return

    def selectRubricByKey(self, key):
        """Select row with given key. Return true if works, else false"""
        if key is None:
            return False
        for r in range(self.rowCount()):
            if int(self.item(r, 0).text()) == int(key):
                self.selectRow(r)
                return True
        return False

    def nextRubric(self):
        """Move selection to the next row, wrapping around if needed."""
        r = self.getCurrentRubricRow()
        if r is None:
            if self.rowCount() >= 1:
                self.selectRubricByVisibleRow(0)
                self.handleClick()
            return
        rs = r
        while True:
            r = (r + 1) % self.rowCount()
            if r == rs or not self.isRowHidden(r):
                break
        self.selectRubricByRow(r)
        self.handleClick()

    def previousRubric(self):
        """Move selection to the prevoous row, wrapping around if needed."""
        r = self.getCurrentRubricRow()
        if r is None:
            if self.rowCount() >= 1:
                self.selectRubricByRow(self.lastUnhiddenRow())
            return
        rs = r
        while True:
            r = (r - 1) % self.rowCount()
            if r == rs or not self.isRowHidden(r):
                break
        self.selectRubricByRow(r)
        self.handleClick()

    def handleClick(self):
        r = self.getCurrentRubricRow()
        if r is None:
            r = self.firstUnhiddenRow()
            if r is None:
                return
            self.selectRubricByRow(r)
        delta = self.item(r, 2).text()
        if self.item(r, 4).text() == 'absolute':
            delta = self.item(r, 2).text()[:-abs_suffix_length]
        self._parent.rubricSignal.emit([delta, self.item(r, 3).text(), self.item(r, 0).text(), self.item(r, 4).text()])

    def firstUnhiddenRow(self):
        for r in range(self.rowCount()):
            if not self.isRowHidden(r):
                return r
        return None

    def lastUnhiddenRow(self):
        for r in reversed(range(self.rowCount())):
            if not self.isRowHidden(r):
                return r
        return None

    def colourLegalRubric(self, r, mss):
        legal = isLegalRubric(mss, kind=self.item(r, 4).text(), delta=self.item(r, 2).text())
        colour_legal = self.palette().color(QPalette.Active, QPalette.Text)
        colour_illegal = self.palette().color(QPalette.Disabled, QPalette.Text)
        if legal == 2:
            self.showRow(r)
            self.item(r, 2).setForeground(colour_legal)
            self.item(r, 3).setForeground(colour_legal)
        elif legal == 1:
            self.showRow(r)
            self.item(r, 2).setForeground(colour_illegal)
            self.item(r, 3).setForeground(colour_illegal)
        else:
            self.hideRow(r)

    def updateLegalityOfDeltas(self, mss):
        """Style items according to their legality based on max,state and score (mss)"""
        for r in range(self.rowCount()):
            self.colourLegalRubric(r, mss)

    def editRow(self, tableIndex):
        r = tableIndex.row()
        rubricKey = self.item(r, 0).text()
        self._parent.edit_rubric(rubricKey)

    def updateRubric(self, new_rubric, mss):
        for r in range(self.rowCount()):
            if self.item(r, 0).text() == new_rubric['id']:
                self.item(r, 1).setText(new_rubric['username'])
                self.item(r, 2).setText(new_rubric['delta'])
                self.item(r, 3).setText(new_rubric['text'])
                self.item(r, 4).setText(new_rubric['kind'])
                self.colourLegalRubric(r, mss)
                hoverText = ''
                if new_rubric['tags'] != '':
                    hoverText += 'Tagged as {}\n'.format(new_rubric['tags'])
                if new_rubric['meta'] != '':
                    hoverText += '{}\n'.format(new_rubric['meta'])
                self.item(r, 3).setToolTip(hoverText.strip())

class TabBarWithAddRenameRemoveContext(QTabBar):
    """A QTabBar with a context right-click menu for add/rename/remove tabs.

    Has slots for add, renaming and removing tabs:

    * add_tab_signal
    * rename_tab_signal
    * remove_tab_signal
    """
    add_tab_signal = pyqtSignal()
    rename_tab_signal = pyqtSignal(int)
    remove_tab_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.RightButton:
            point = mouseEvent.pos()
            n = self.tabAt(point)
            if n >= 0:
                name = self.tabText(n)
                menu = QMenu()
                menu.addAction(f'Rename tab "{name}"...', lambda: self.rename_tab_signal.emit(n))
                menu.addAction(f'Remove tab "{name}"...', lambda: self.remove_tab_signal.emit(n))
                menu.addAction('Add new tab', self.add_tab_signal.emit)
                menu.exec(self.mapToGlobal(point))
        super().mousePressEvent(mouseEvent)

class RubricWidget(QWidget):
    """The RubricWidget is a multi-tab interface for displaying, choosing and managing rubrics."""
    rubricSignal = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)
        self.question_number = None
        self._parent = parent
        self.username = parent.username
        self.rubrics = []
        self.maxMark = None
        self.currentScore = None
        self.currentState = None
        self.mss = [self.maxMark, self.currentState, self.currentScore]
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        deltaP_label = '+δ'
        deltaN_label = '−δ'
        self.tabS = RubricTable(self, shortname='Shared', tabType='show')
        self.tabDeltaP = RubricTable(self, shortname=deltaP_label, tabType='delta')
        self.tabDeltaN = RubricTable(self, shortname=deltaN_label, tabType='delta')
        self.RTW = QTabWidget()
        tb = TabBarWithAddRenameRemoveContext()
        tb.add_tab_signal.connect(self.add_new_tab)
        tb.rename_tab_signal.connect(self.rename_tab)
        tb.remove_tab_signal.connect(self.remove_tab)
        self.RTW.setTabBar(tb)
        self.RTW.setMovable(True)
        self.RTW.tabBar().setChangeCurrentOnDrag(True)
        self.RTW.addTab(self.tabS, self.tabS.shortname)
        self.RTW.addTab(self.tabDeltaP, self.tabDeltaP.shortname)
        self.RTW.addTab(self.tabDeltaN, self.tabDeltaN.shortname)
        b = QToolButton()
        b.setText('+')
        b.setAutoRaise(True)
        b.clicked.connect(self.add_new_tab)
        m = QMenu()
        m.addAction('Add tab', self.add_new_tab)
        m.addAction('Rename current tab...', self.rename_current_tab)
        m.addSeparator()
        m.addAction('Remove current tab...', self.remove_current_tab)
        b.setMenu(m)
        self.RTW.setCornerWidget(b)
        self.RTW.setCurrentIndex(0)
        self.RTW.currentChanged.connect(self.handleClick)
        self.tabHide = RubricTable(self, sort=True, tabType='hide')
        self.groupHide = QTabWidget()
        self.groupHide.addTab(self.tabHide, 'Hidden')
        self.showHideW = QStackedWidget()
        self.showHideW.addWidget(self.RTW)
        self.showHideW.addWidget(self.groupHide)
        grid.addWidget(self.showHideW, 1, 1, 2, 4)
        self.addB = QPushButton('Add')
        self.filtB = QPushButton('Arrange/Filter')
        self.hideB = QPushButton('Shown/Hidden')
        self.syncB = QToolButton()
        self.syncB.setText('Sync')
        self.syncB.setToolTip('Synchronise rubrics')
        grid.addWidget(self.addB, 3, 1)
        grid.addWidget(self.filtB, 3, 2)
        grid.addWidget(self.hideB, 3, 3)
        grid.addWidget(self.syncB, 3, 4)
        grid.setSpacing(0)
        self.setLayout(grid)
        self.addB.clicked.connect(self.add_new_rubric)
        self.filtB.clicked.connect(self.wrangleRubricsInteractively)
        self.syncB.clicked.connect(self.refreshRubrics)
        self.hideB.clicked.connect(self.toggleShowHide)

    def toggleShowHide(self):
        if self.showHideW.currentIndex() == 0:
            self.showHideW.setCurrentIndex(1)
            self.addB.setEnabled(False)
            self.filtB.setEnabled(False)
            self.syncB.setEnabled(False)
            self.tabHide.handleClick()
        else:
            self.showHideW.setCurrentIndex(0)
            self.addB.setEnabled(True)
            self.filtB.setEnabled(True)
            self.syncB.setEnabled(True)
            self.handleClick()

    @property
    def user_tabs(self):
        """Dynamically construct the ordered list of user-defined tabs."""
        L = []
        for n in range(self.RTW.count()):
            tab = self.RTW.widget(n)
            if tab.is_user_tab():
                L.append(tab)
        return L

    def update_tab_names(self):
        """Loop over the tabs and update their displayed names"""
        for n in range(self.RTW.count()):
            self.RTW.setTabText(n, self.RTW.widget(n).shortname)

    def add_new_tab(self, name=None):
        """Add new user-defined tab either to end or near end.

        The new tab is inserted after the right-most non-delta tab.
        For example, the default config has delta tabs at the end; if
        user adds a new tab, it appears before these.  But the user may
        have rearranged the delta tabs left of their custom tabs.

        args:
            name (str/None): name of the new tab.  If omitted or None,
                generate one from a set of symbols with digits appended
                if necessary.
        """
        if not name:
            tab_names = [x.shortname for x in self.user_tabs]
            name = next_in_longest_subsequence(tab_names)
        if not name:
            syms = ('★', '♥', '♠', '♦', '♣', '‡', '❦', '❧')
            extra = ''
            counter = 0
            while not name:
                for s in syms:
                    if s + extra not in tab_names:
                        name = s + extra
                        break
                counter += 1
                extra = f'{counter}'
        tab = RubricTable(self, shortname=name)
        n = self.RTW.count() - 1
        while self.RTW.widget(n).is_delta_tab() and n > 0:
            n = n - 1
        self.RTW.insertTab(n + 1, tab, tab.shortname)

    def remove_current_tab(self):
        n = self.RTW.currentIndex()
        self.remove_tab(n)

    def remove_tab(self, n):
        if n < 0:
            return
        tab = self.RTW.widget(n)
        if not tab:
            return
        if not tab.is_user_tab():
            return
        if tab.rowCount() > 0:
            msg = '<p>Are you sure you want to delete the '
            msg += f'tab &ldquo;{tab.shortname}&rdquo;?</p>'
            msg += '<p>(The rubrics themselves will not be deleted).<p>'
        else:
            msg = '<p>Are you sure you want to delete the empty '
            msg += f'tab &ldquo;{tab.shortname}&rdquo;?</p>'
        if SimpleQuestion(self, msg).exec() == QMessageBox.No:
            return
        self.RTW.removeTab(n)
        tab.clear()
        tab.deleteLater()

    def rename_current_tab(self):
        n = self.RTW.currentIndex()
        self.rename_tab(n)

    def rename_tab(self, n):
        if n < 0:
            return
        tab = self.RTW.widget(n)
        if not tab:
            return
        if tab.is_delta_tab():
            return
        curname = tab.shortname
        s, ok = QInputDialog.getText(self, f'Rename tab "{curname}"', f'Enter new name for tab "{curname}"')
        if not ok:
            return
        log.debug('changing tab name from "%s" to "%s"', curname, s)
        tab.set_name(s)

    def refreshRubrics(self):
        """Get rubrics from server and if non-trivial then repopulate"""
        old_rubrics = self.rubrics
        self.rubrics = self._parent.getRubricsFromServer()
        self.setRubricTabsFromState(self.get_tab_rubric_lists())
        self._parent.saveTabStateToServer(self.get_tab_rubric_lists())
        msg = '<p>✓ Your tabs have been synced to the server.</p>\n'
        diff = set((d['id'] for d in self.rubrics)) - set((d['id'] for d in old_rubrics))
        if not diff:
            msg += '<p>✓ No new rubrics are available.</p>\n'
        else:
            msg += f'<p>✓ <b>{len(diff)} new rubrics</b> have been downloaded from the server:</p>\n'
            diff = [r for r in self.rubrics for i in diff if r['id'] == i]
            ell = '…'
            abbrev = []
            display_at_most = 12
            for n, r in enumerate(diff):
                delta = '.&nbsp;' if r['delta'] == '.' else r['delta']
                text = html.escape(shorten(r['text'], 36, placeholder=ell))
                render = f"<li><tt>{delta}</tt> <i>&ldquo;{text}&rdquo;</i>&nbsp; by {r['username']}</li>"
                if n < display_at_most - 1:
                    abbrev.append(render)
                elif n == display_at_most - 1 and len(diff) == display_at_most:
                    abbrev.append(render)
                elif n == display_at_most - 1:
                    abbrev.append('<li>' + '&nbsp;' * 6 + '⋮</li>')
                    break
            msg += '<ul style="list-style-type:none;">\n  {}\n</ul>'.format('\n  '.join(abbrev))
        QMessageBox(QMessageBox.Information, 'Finished syncing rubrics', msg, QMessageBox.Ok, self).exec()
        self.updateLegalityOfDeltas()

    def wrangleRubricsInteractively(self):
        wr = RubricWrangler(self, self.rubrics, self.get_tab_rubric_lists(), self.username, annotator_size=self._parent.size())
        if wr.exec() != QDialog.Accepted:
            return
        else:
            self.setRubricTabsFromState(wr.wranglerState)

    def setInitialRubrics(self, user_tab_state=None):
        """Grab rubrics from server and set sensible initial values.

        Note: must be called after annotator knows its tgv etc, so
        maybe difficult to call from __init__.  TODO: a possible
        refactor would have the caller (which is probably `_parent`)
        get the server rubrics list and pass in as an argument.

        args:
            wranglerState (dict/None): a representation of the state of
                the user's tabs, or None.  If None then pull from server.
                If server also has none, initialize with some empty tabs.
                Note: currently caller always passes None.
        """
        self.rubrics = self._parent.getRubricsFromServer()
        if not user_tab_state:
            user_tab_state = self._parent.getTabStateFromServer()
        if not user_tab_state:
            self.add_new_tab()
        self.setRubricTabsFromState(user_tab_state)

    def setRubricTabsFromState(self, wranglerState=None):
        """Set rubric tabs (but not rubrics themselves) from saved data.

        The various rubric tabs are updated based on data passed in.
        The rubrics themselves are uneffected.

        args:
            wranglerState (dict/None): a representation of the state of
                the user's tabs.  This could be from a previous session
                or it could be "stale" in the sense that new rubrics
                have arrived or some have been deleted.  Can be None
                meaning no state.
                The contents must contain lists `shown`, `hidden`,
                `tabs`, and `user_tab_names`.  The last two are lists of
                lists.  Any of these could be empty.

        If there is too much data for the number of tabs, the extra data
        is discarded.  If there is too few data, pad with empty lists
        and/or leave the current lists as they are.
        """
        if not wranglerState:
            wranglerState = {'user_tab_names': [], 'shown': [], 'hidden': [], 'tabs': []}
        for rubric in self.rubrics:
            if rubric['username'] == 'HAL':
                continue
            if rubric['username'] == 'manager' and rubric['kind'] == 'delta':
                continue
            if rubric['id'] not in wranglerState['hidden'] and rubric['id'] not in wranglerState['shown']:
                log.info('Appending new rubric with id {}'.format(rubric['id']))
                wranglerState['shown'].append(rubric['id'])
        curtabs = self.user_tabs
        newnames = wranglerState['user_tab_names']
        for n in range(max(len(curtabs), len(newnames))):
            if n < len(curtabs):
                if n < len(newnames):
                    curtabs[n].set_name(newnames[n])
            elif n < len(newnames):
                self.add_new_tab(newnames[n])
        del curtabs
        for n, tab in enumerate(self.user_tabs):
            if n >= len(wranglerState['tabs']):
                idlist = []
            else:
                idlist = wranglerState['tabs'][n]
            tab.setRubricsByKeys(self.rubrics, idlist)
        self.tabS.setRubricsByKeys(self.rubrics, wranglerState['shown'])
        self.tabDeltaP.setDeltaRubrics(self.rubrics, positive=True)
        self.tabDeltaN.setDeltaRubrics(self.rubrics, positive=False)
        self.tabHide.setRubricsByKeys(self.rubrics, wranglerState['hidden'])
        self.tabHide.selectRubricByVisibleRow(0)
        self.tabDeltaP.selectRubricByVisibleRow(0)
        self.tabDeltaN.selectRubricByVisibleRow(0)
        self.tabS.selectRubricByVisibleRow(0)
        for tab in self.user_tabs:
            tab.selectRubricByVisibleRow(0)

    def getCurrentRubricKeyAndTab(self):
        """return the current rubric key and the current tab.

        returns:
            list: [a,b] where a=rubric-key=(int/none) and b=current tab index = int
        """
        return [self.RTW.currentWidget().getCurrentRubricKey(), self.RTW.currentIndex()]

    def setCurrentRubricKeyAndTab(self, key, tab):
        """set the current rubric key and the current tab

        args
            key (int/None): which rubric to highlight.  If no None, no action.
            tab (int): which tab to choose.

        returns:
            bool: True if we set a row, False if we could not find an appropriate row
                b/c for example key or tab are invalid or not found.
        """
        if key is None:
            return False
        if tab in range(0, self.RTW.count()):
            self.RTW.setCurrentIndex(tab)
        else:
            return False
        return self.RTW.currentWidget().selectRubricByKey(key)

    def setQuestionNumber(self, qn):
        """Set question number being graded.

        args:
            qn (int/None): the question number.
        """
        self.question_number = qn

    def reset(self):
        """Return the widget to a no-TGV-specified state."""
        self.setQuestionNumber(None)
        log.debug('TODO - what else needs doing on reset')

    def changeMark(self, currentScore, currentState, maxMark=None):
        if maxMark:
            self.maxMark = maxMark
        self.currentScore = currentScore
        self.currentState = currentState
        self.mss = [self.maxMark, self.currentState, self.currentScore]
        self.updateLegalityOfDeltas()

    def updateLegalityOfDeltas(self):
        self.tabS.updateLegalityOfDeltas(self.mss)
        for tab in self.user_tabs:
            tab.updateLegalityOfDeltas(self.mss)
        self.tabDeltaP.updateLegalityOfDeltas(self.mss)
        self.tabDeltaN.updateLegalityOfDeltas(self.mss)

    def handleClick(self):
        self.RTW.currentWidget().handleClick()

    def reselectCurrentRubric(self):
        self.RTW.currentWidget().reselectCurrentRubric()
        self.handleClick()

    def selectRubricByRow(self, rowNumber):
        self.RTW.currentWidget().selectRubricByRow(rowNumber)
        self.handleClick()

    def selectRubricByVisibleRow(self, rowNumber):
        self.RTW.currentWidget().selectRubricByVisibleRow(rowNumber)
        self.handleClick()

    def getCurrentTabName(self):
        return self.RTW.currentWidget().shortname

    def nextRubric(self):
        if self.showHideW.currentIndex() == 0:
            self.RTW.currentWidget().nextRubric()
        else:
            self.tabHide.nextRubric()

    def previousRubric(self):
        if self.showHideW.currentIndex() == 0:
            self.RTW.currentWidget().previousRubric()
        else:
            self.tabHide.previousRubric()

    def next_tab(self):
        """Move to next tab, only if tabs are shown."""
        if self.showHideW.currentIndex() == 0:
            numtabs = self.RTW.count()
            nt = (self.RTW.currentIndex() + 1) % numtabs
            self.RTW.setCurrentIndex(nt)

    def prev_tab(self):
        """Move to previous tab, only if tabs are shown."""
        if self.showHideW.currentIndex() == 0:
            numtabs = self.RTW.count()
            pt = (self.RTW.currentIndex() - 1) % numtabs
            self.RTW.setCurrentIndex(pt)

    def get_nonrubric_text_from_page(self):
        """Find any text that isn't already part of a formal rubric.

        Returns:
            list: strings for each text on page that is not inside a rubric
        """
        return self._parent.get_nonrubric_text_from_page()

    def unhideRubricByKey(self, key):
        index = [x['id'] for x in self.rubrics].index(key)
        self.tabS.appendNewRubric(self.rubrics[index])

    def hideRubricByKey(self, key):
        index = [x['id'] for x in self.rubrics].index(key)
        self.tabHide.appendNewRubric(self.rubrics[index])

    def add_new_rubric(self):
        """Open a dialog to create a new comment."""
        self._new_or_edit_rubric(None)

    def edit_rubric(self, key):
        """Open a dialog to edit a rubric - from the id-key of that rubric."""
        try:
            index = [x['id'] for x in self.rubrics].index(key)
        except ValueError:
            return
        com = self.rubrics[index]
        if com['username'] == self.username:
            self._new_or_edit_rubric(com, edit=True, index=index)
            return
        msg = SimpleQuestion(self, f"<p>You did not create this rubric (it was created by &ldquo;{com['username']}&rdquo;).</p>", 'Do you want to make a copy and edit that instead?')
        if msg.exec() == QMessageBox.No:
            return
        com = com.copy()
        newmeta = [com['meta']] if com['meta'] else []
        newmeta.append('Forked from Rubric ID {}, created by user "{}".'.format(com['id'], com['username']))
        com['meta'] = '\n'.join(newmeta)
        com['id'] = None
        com['username'] = self.username
        self._new_or_edit_rubric(com, edit=False)

    def _new_or_edit_rubric(self, com, edit=False, index=None):
        """Open a dialog to edit a comment or make a new one.

        args:
            com (dict/None): a comment to modify or use as a template
                depending on next arg.  If set to None, which always
                means create new.
            edit (bool): are we modifying the comment?  if False, use
                `com` as a template for a new duplicated comment.
            index (int): the index of the comment inside the current rubric list
                used for updating the data in the rubric list after edit (only)

        Returns:
            None: does its work through side effects on the comment list.
        """
        if self.question_number is None:
            log.error('Not allowed to create rubric while question number undefined.')
            return
        reapable = self.get_nonrubric_text_from_page()
        arb = AddRubricBox(self, self.username, self.maxMark, reapable, com, annotator_size=self._parent.size())
        if arb.exec() != QDialog.Accepted:
            return
        if arb.DE.checkState() == Qt.Checked:
            dlt = str(arb.SB.textFromValue(arb.SB.value()))
        else:
            dlt = '.'
        txt = arb.TE.toPlainText().strip()
        tag = arb.TEtag.toPlainText().strip()
        meta = arb.TEmeta.toPlainText().strip()
        kind = arb.Lkind.text().strip()
        username = arb.Luser.text().strip()
        rubricID = arb.label_rubric_id.text().strip()
        new_rubric = {'kind': kind, 'delta': dlt, 'text': txt, 'tags': tag, 'meta': meta, 'username': self.username, 'question': self.question_number}
        if edit:
            new_rubric['id'] = rubricID
            rv = self._parent.modifyRubric(rubricID, new_rubric)
            assert self.rubrics[index]['id'] == new_rubric['id']
            self.rubrics[index] = new_rubric
            self.updateRubricInLists(new_rubric)
        else:
            rv = self._parent.createNewRubric(new_rubric)
            if not rv[0]:
                return
            rubricID = rv[1]
            new_rubric['id'] = rubricID
            self.rubrics.append(new_rubric)
            self.tabS.appendNewRubric(new_rubric)
            if self.RTW.currentWidget().is_user_tab():
                self.RTW.currentWidget().appendNewRubric(new_rubric)
        self.RTW.currentWidget().selectRubricByKey(rubricID)
        self.handleClick()

    def updateRubricInLists(self, new_rubric):
        self.tabS.updateRubric(new_rubric, self.mss)
        self.tabHide.updateRubric(new_rubric, self.mss)
        for tab in self.user_tabs:
            tab.updateRubric(new_rubric, self.mss)

    def get_tab_rubric_lists(self):
        """returns a dict of lists of the current rubrics"""
        return {'user_tab_names': [t.shortname for t in self.user_tabs], 'shown': self.tabS.getKeyList(), 'hidden': self.tabHide.getKeyList(), 'tabs': [t.getKeyList() for t in self.user_tabs]}

class SignedSB(QSpinBox):

    def __init__(self, maxMark):
        super().__init__()
        self.setRange(-maxMark, maxMark)
        self.setValue(1)

    def stepBy(self, steps):
        self.setValue(self.value() + steps)
        if self.value() == 0:
            self.setValue(self.value() + steps)

    def textFromValue(self, n):
        t = QSpinBox().textFromValue(n)
        if n > 0:
            return '+' + t
        else:
            return t

class AddRubricBox(QDialog):

    def __init__(self, parent, username, maxMark, lst, com=None, annotator_size=None):
        """Initialize a new dialog to edit/create a comment.

        Args:
            parent (QWidget): the parent window.
            username (str)
            maxMark (int)
            lst (list): these are used to "harvest" plain 'ol text
                annotations and morph them into comments.
            com (dict/None): if None, we're creating a new rubric.
                Otherwise, this has the current comment data.
            annotator_size (QSize/None): size of the parent annotator
        """
        super().__init__(parent)
        if com:
            self.setWindowTitle('Modify rubric')
        else:
            self.setWindowTitle('Add new rubric')
        if annotator_size:
            self.resize(annotator_size / 2)
        self.CB = QComboBox()
        self.TE = QTextEdit()
        self.SB = SignedSB(maxMark)
        self.DE = QCheckBox('enabled')
        self.DE.setCheckState(Qt.Checked)
        self.DE.stateChanged.connect(self.toggleSB)
        self.TEtag = QTextEdit()
        self.TEmeta = QTextEdit()
        self.label_rubric_id = QLabel('Will be auto-assigned')
        self.Luser = QLabel()
        self.Lkind = QLabel('relative')
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setVerticalStretch(3)
        self.TE.setSizePolicy(sizePolicy)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setVerticalStretch(1)
        self.TEtag.setSizePolicy(sizePolicy)
        self.TEmeta.setSizePolicy(sizePolicy)
        flay = QFormLayout()
        flay.addRow('Enter text', self.TE)
        lay = QFormLayout()
        lay.addRow('or choose text', self.CB)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.CB.setSizePolicy(sizePolicy)
        flay.addRow('', lay)
        lay = QHBoxLayout()
        lay.addWidget(self.DE)
        lay.addItem(QSpacerItem(48, 10, QSizePolicy.Preferred, QSizePolicy.Minimum))
        lay.addWidget(self.SB)
        flay.addRow('Delta mark', lay)
        flay.addRow('Tags', self.TEtag)
        flay.addRow('Meta', self.TEmeta)
        flay.addRow('kind', self.Lkind)
        flay.addRow('Rubric ID', self.label_rubric_id)
        flay.addRow('User who created', self.Luser)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        vlay = QVBoxLayout()
        vlay.addLayout(flay)
        vlay.addWidget(buttons)
        self.setLayout(vlay)
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        self.CB.addItem('')
        self.CB.addItems(lst)
        self.CB.currentTextChanged.connect(self.changedCB)
        if com:
            if com['text']:
                self.TE.clear()
                self.TE.insertPlainText(com['text'])
            if com['tags']:
                self.TEtag.clear()
                self.TEtag.insertPlainText(com['tags'])
            if com['meta']:
                self.TEmeta.clear()
                self.TEmeta.insertPlainText(com['meta'])
            if com['delta']:
                if com['delta'] in ['.', 0, '0']:
                    self.SB.setValue(1)
                    self.DE.setCheckState(Qt.Unchecked)
                else:
                    self.SB.setValue(int(com['delta']))
            if com['id']:
                self.label_rubric_id.setText(str(com['id']))
            if com['username']:
                self.Luser.setText(com['username'])
        else:
            self.TE.setPlaceholderText('Your rubric must contain some text.\n\nPrepend with "tex:" to use latex.\n\nYou can "choose text" to harvest existing text from the page.\n\nChange "delta" below to associate a point-change.')
            self.TEtag.setPlaceholderText('For any user tags you might want. (mostly future use)')
            self.TEmeta.setPlaceholderText('Notes about this rubric such as hints on when to use it.\n\nNot shown to student!')
            self.Luser.setText(username)

    def changedCB(self):
        self.TE.clear()
        self.TE.insertPlainText(self.CB.currentText())

    def toggleSB(self):
        if self.DE.checkState() == Qt.Checked:
            self.SB.setEnabled(True)
            self.Lkind.setText('relative')
            if self.SB.value() == 0:
                self.SB.setValue(1)
        else:
            self.Lkind.setText('neutral')
            self.SB.setEnabled(False)

    def validate_and_accept(self):
        """Make sure rubric is valid before accepting"""
        if len(self.TE.toPlainText().strip()) <= 0:
            WarnMsg(self, 'Your rubric must contain some text.').exec()
            return
        if self.SB.value() == 0 and self.DE.checkState() == Qt.Checked:
            WarnMsg(self, "If 'Delta mark' is checked then the rubric cannot have a delta of zero.").exec()
            return
        self.accept()