from PyQt6.QtWidgets import QTableView
from models.org_table_model import OrgTableModel


class StaffView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeMode.ResizeToContents)

        self._model = OrgTableModel(self)
        self.setModel(self._model)

    @property
    def model(self):
        return self._model

    def refresh(self):
        pass
