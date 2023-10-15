from PyQt6.QtWidgets import QTreeView
from PyQt6.QtCore import QObject, QModelIndex
from models.org_model import OrgModel


class OrgsView(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._model = OrgModel(parent=self)

        item1 = QObject()
        item1.setProperty("Код".encode("utf8"), "1")
        item1.setProperty("Наименование".encode("utf8"), "Father")
        item2 = QObject(parent=item1)
        item2.setProperty("Код".encode("utf8"), "1.1")
        item2.setProperty("Наименование".encode("utf8"), "Son")
        self._model.add_item(item1, QModelIndex())

        self.setModel(self._model)
