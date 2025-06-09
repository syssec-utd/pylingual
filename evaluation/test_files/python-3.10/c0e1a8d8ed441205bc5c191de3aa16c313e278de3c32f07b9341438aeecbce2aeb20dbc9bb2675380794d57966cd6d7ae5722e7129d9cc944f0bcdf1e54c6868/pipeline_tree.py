from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import Qt
from SciQLop.backend.models import pipelines
from ..common import TreeView

class PipelineTree(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PipelineTree, self).__init__(parent)
        self._model_proxy = QtCore.QSortFilterProxyModel(self)
        self._model_proxy.setSourceModel(pipelines)
        self._view = TreeView(self)
        self._view.setModel(self._model_proxy)
        self._view.setSortingEnabled(False)
        self._model_proxy.setFilterRole(QtCore.Qt.UserRole)
        self._model_proxy.setRecursiveFilteringEnabled(True)
        self._model_proxy.setAutoAcceptChildRows(True)
        self._filter = QtWidgets.QLineEdit(self)
        self._filter.setClearButtonEnabled(True)
        self._filter.addAction(QtGui.QIcon(':/icons/zoom.png'), QtWidgets.QLineEdit.LeadingPosition)
        self._filter.setPlaceholderText('Search...')
        self._completer = QtWidgets.QCompleter(self)
        self._completer.setModel(pipelines.completion_model)
        self._completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self._completer.setModelSorting(QtWidgets.QCompleter.CaseSensitivelySortedModel)
        self._filter.setCompleter(self._completer)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self._filter)
        self.layout().addWidget(self._view)
        self._filter.editingFinished.connect(lambda : self._model_proxy.setFilterFixedString(self._filter.text()))
        self.setWindowTitle('Pipelines')
        self._selection_model = self._view.selectionModel()
        self._selection_model.selectionChanged.connect(lambda a, b: pipelines.select(list(map(self._model_proxy.mapToSource, self._view.selectedIndexes()))))

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            pipelines.delete(list(map(self._model_proxy.mapToSource, self._view.selectedIndexes())))