from PyQt6.QtWidgets import QTreeView
from PyQt6.QtCore import QModelIndex, pyqtSignal, pyqtSlot
from models.org_model import OrgModel


class OrgsView(QTreeView):

    org_selected = pyqtSignal(QModelIndex)

    # @pyqtSlot(QModelIndex)
    # def select_child(self, index: QModelIndex):
    #     self._model.get_children(index)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.SingleSelection)

        self._model = OrgModel(parent=self)
        self._model.init_model()
        self.setModel(self._model)
        self.hideColumn(2)

        header = self.header()
        header.setSectionResizeMode(header.ResizeMode.ResizeToContents)
        #self.org_selected.connect(self.select_child)

    @property
    def model(self):
        return self._model

    def currentChanged(self, current: QModelIndex, previous: QModelIndex) -> None:
        if current.isValid():
            self.org_selected.emit(current)

