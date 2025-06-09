""" Table Widget enhancement to simplify "key=value" style tables
Copyright Nanosurf AG 2021
License - MIT
"""
import enum
import typing
from nanosurf.lib.gui.import_helper import import_pyside2_if_none_is_detected
if import_pyside2_if_none_is_detected():
    from PySide2 import QtWidgets, QtCore
else:
    from PySide6 import QtWidgets, QtCore
import nanosurf.lib.datatypes.sci_val as sci_val

class TableEntryIDs(enum.IntEnum):
    """
   Subclass this enum class and define a identifier for each table entry
   First entry must have index 0. eg MyFirstVal = 0
   Then define each TableEntryID by NSFNameValueTable.define_entry() during gui preparation
   """
    pass

class NSFNameValueTable(QtWidgets.QTableWidget):

    def __init__(self, table_entry_ids: TableEntryIDs, parent: QtWidgets.QWidget=None) -> None:
        super().__init__()
        self.setEnabled(False)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Name', 'Value'])
        self.define_table(table_entry_ids)

    def define_table(self, table_entry_ids: TableEntryIDs):
        self._table_ids = table_entry_ids
        self.setRowCount(len(list(self._table_ids)))
        self.setMinimumSize(0, (self.rowCount() + 1) * 30)

    def define_entry(self, entry_id: TableEntryIDs, name: str, value: str='-') -> None:
        self.setItem(entry_id, 0, QtWidgets.QTableWidgetItem(name))
        self.setItem(entry_id, 1, QtWidgets.QTableWidgetItem(value))

    def clear_values(self, value_default: str='-') -> None:
        for id in self._table_ids:
            self.item(id, 1).setText(value_default)

    def clear_value(self, entry_id: TableEntryIDs, value_default: str='-') -> None:
        self.item(entry_id, 1).setText(value_default)

    def get_entry_count(self):
        return len(list(self._table_ids))

    def set_value(self, entry_id: TableEntryIDs, value, unit='', precision=3):
        str_val = ''
        if isinstance(value, sci_val.SciVal):
            str_val = value.to_string_formatted(sci_val.up.Prefix.auto_, precision=precision)
        elif isinstance(value, str):
            str_val = value
        else:
            val = sci_val.SciVal(value, unit_str=unit)
            str_val = val.to_string_formatted(sci_val.up.Prefix.auto_, precision=precision)
        self.item(entry_id, 1).setText(str_val)

    def get_value(self, entry_id: TableEntryIDs) -> sci_val.SciVal:
        val_str = self.item(entry_id, 1).text()
        res = sci_val.convert.to_value(val_str)
        if res.success:
            return sci_val.SciVal(res.value, res.unit)
        return sci_val.SciVal(0.0, '')

class NSFTable(QtWidgets.QTableWidget):

    def __init__(self, header: list[str], initial_entries=1, hide_header: bool=False, parent: QtWidgets.QWidget=None) -> None:
        super().__init__(parent)
        self.setEnabled(False)
        self.verticalHeader().hide()
        if hide_header:
            self.horizontalHeader().hide()
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)
        self.define_table(initial_entries)
        self.setMinimumSize(0, (self.rowCount() + 1) * 30)

    def define_table(self, entries: int):
        current_len = self.rowCount()
        items = ['' for _ in range(self.columnCount())]
        self.setRowCount(entries)
        for new_entry in range(current_len, entries):
            self.define_entry(new_entry, items)

    def define_entry(self, entry_id: int, items: list[str], flags: QtCore.Qt.ItemFlag=QtCore.Qt.ItemFlag.ItemIsSelectable) -> None:
        for (col_index, value) in enumerate(items):
            self.setItem(entry_id, col_index, QtWidgets.QTableWidgetItem(value))
            self.item(entry_id, col_index).setFlags(flags)

    def clear_values(self, value_default: str='') -> None:
        for index in range(self.rowCount()):
            self.clear_value(index, value_default)

    def clear_value(self, entry_id: int, value_default: str='') -> None:
        for col_index in range(self.columnCount()):
            self.item(entry_id, col_index).setText(value_default)

    def set_entry_flags(self, entry_id: int, col_index: int, flags: QtCore.Qt.ItemFlag) -> None:
        self.item(entry_id, col_index).setFlags(flags)

    def set_column_flags(self, col_index: int, flags: QtCore.Qt.ItemFlag) -> None:
        for row_index in range(self.rowCount()):
            self.item(row_index, col_index).setFlags(flags)
            if QtCore.Qt.ItemFlag.ItemIsUserCheckable & flags:
                self.item(row_index, col_index).setCheckState(QtCore.Qt.CheckState.Unchecked)

    def get_entry_count(self):
        return self.rowCount()

    def set_value(self, entry_id: TableEntryIDs, col_pos: int, value: typing.Union[str, sci_val.SciVal, int, float], unit: str='', precision: int=3):
        str_val = ''
        if isinstance(value, sci_val.SciVal):
            str_val = value.to_string_formatted(sci_val.up.Prefix.auto_, precision=precision)
        elif isinstance(value, str):
            str_val = value
        else:
            val = sci_val.SciVal(value, unit_str=unit)
            str_val = val.to_string_formatted(sci_val.up.Prefix.auto_, precision=precision)
        self.item(entry_id, col_pos).setText(str_val)

    def get_value(self, entry_id: int, col_pos: int) -> str:
        val_str = self.item(entry_id, col_pos).text()
        return val_str