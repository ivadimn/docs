from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSlot, QModelIndex, Qt
from .orgs_view import OrgsView


class OrgFrame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.orgs_view = OrgsView(parent=self)
        self.orgs_view.org_selected.connect(self.org_view_changed)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.orgs_view)
        self.setLayout(hbox)

    @pyqtSlot(QModelIndex)
    def org_view_changed(self, current: QModelIndex):
        self.orgs_view.model.get_children(current)
        #self.staff_view.model.refresh
        org = current.data(Qt.ItemDataRole.UserRole+0)
        print(org)

