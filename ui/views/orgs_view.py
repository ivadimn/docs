from PyQt6.QtWidgets import QTreeView, QHeaderView
from PyQt6.QtCore import QObject, QModelIndex, Qt, pyqtSignal, pyqtSlot
from models.org_model import OrgModel


class OrgsView(QTreeView):

    org_selected = pyqtSignal(QModelIndex)

    @pyqtSlot(QModelIndex)
    def select_child(self, index: QModelIndex):
        self._model.get_children(index)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.SingleSelection)

        self._model = OrgModel(parent=self)
        self._model.init_model()
        self.setModel(self._model)
        self.hideColumn(2)
        self.setAlternatingRowColors(True)
        header = QHeaderView(Qt.Orientation.Horizontal, self)

        self.setHeader(header)
        self.org_selected.connect(self.select_child)

    def currentChanged(self, current: QModelIndex, previous: QModelIndex) -> None:
        if current.isValid():
            self.org_selected.emit(current)

