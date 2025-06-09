from __future__ import annotations
from typing import TYPE_CHECKING, cast
from qtpy import QtWidgets as QtW, QtGui
from qtpy.QtCore import Qt, Signal
if TYPE_CHECKING:
    from ._table_base import QBaseTable
    from ._enhanced_table import _QTableViewEnhanced
    from ..._table_stack import QTabbedTableStack

class QTableGroup(QtW.QSplitter):
    """Split view of two tables."""
    focusChanged = Signal(int)

    def __init__(self, tables: list[QBaseTable], orientation=Qt.Orientation.Horizontal):
        super().__init__(orientation)
        self.setChildrenCollapsible(False)
        self._tables: list[QBaseTable] = []
        for (i, table) in enumerate(tables):
            view_copy = table._central_widget.copy(link=True)
            view_copy.focusedSignal.connect(lambda : self.focusChanged.emit(self.focusedIndex()))
            self.addWidget(view_copy)
            self.setStretchFactor(i, 1)
            self._tables.append(table)
        self.focusChanged.connect(self._on_focus_changed)

    def copy(self) -> QTableGroup:
        """Make a copy of this widget."""
        copy = self.__class__(self.tables, self.orientation())
        return copy

    @property
    def tables(self) -> list[QBaseTable]:
        """List of tables."""
        return self._tables.copy()

    def pop(self, index: int=-1) -> QBaseTable:
        """Pop a table from the group."""
        if index < 0:
            index += self.count()
        out = self._tables.pop(index)
        table = self.widget(index)
        table._selection_model.moving.disconnect(table._on_moving)
        table._selection_model.moved.disconnect(table._on_moved)
        table.deleteLater()
        table.setParent(None)
        return out

    def tableIndex(self, table: QBaseTable) -> int:
        """Return the index of a table in the group."""
        model = table.model()
        for t in self.tables:
            if t.model() is model:
                return t
        raise ValueError('Table not found.')

    def focusedIndex(self) -> int:
        """Return the index of the currently focused table."""
        for i in range(self.count()):
            if self.tableHasFocus(i):
                return i
        return -1

    def setFocusedIndex(self, index: int) -> None:
        """Set the focused widget to the table at index."""
        for i in range(self.count()):
            if i != index:
                self.widget(i).setBackgroundRole(QtGui.QPalette.ColorRole.Dark)
            else:
                self.widget(i).setBackgroundRole(QtGui.QPalette.ColorRole.Light)
        return self.widget(index).setFocus()

    def focusedTable(self) -> QBaseTable | None:
        """Return the currently focused table widget."""
        i = self.focusedIndex()
        if i < 0:
            return None
        return self.tables[i]

    def tableHasFocus(self, index: int) -> bool:
        """True if the table at index has focus."""
        return self.widget(index).hasFocus()

    def __eq__(self, other: QTableGroup) -> bool:
        if not isinstance(other, QTableGroup):
            return False
        return self._tables[0].model() is other._tables[0].model()

    def _on_focus_changed(self, idx: int):
        stack = self.tableStack()
        try:
            idx_dst = stack._group_index_to_tab_index(self, idx)
        except ValueError:
            return
        dst = cast(QTableGroup, stack.widget(idx_dst))
        self.blockSignals(True)
        dst.blockSignals(True)
        stack.setCurrentIndex(idx_dst)
        dst.setFocusedIndex(idx)
        dst.blockSignals(False)
        self.blockSignals(False)

    def tableStack(self) -> QTabbedTableStack:
        return self.parent().parent()

    def deleteLater(self) -> None:
        for i in range(self.count()):
            qtableview = self.widget(i)
            qtableview._selection_model.moving.disconnect(qtableview._on_moving)
            qtableview._selection_model.moved.disconnect(qtableview._on_moved)
        return super().deleteLater()
    if TYPE_CHECKING:

        def widget(self, index: int) -> _QTableViewEnhanced:
            ...