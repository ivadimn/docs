from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt6.QtCore import pyqtSlot, QModelIndex, Qt
from .orgs_view import OrgsView
from .staff_view import StaffView


class OrgFrame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.orgs_view = OrgsView(parent=self)
        self.orgs_view.org_selected.connect(self.org_view_changed)
        self.staff_view = StaffView(self)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.orgs_view)
        splitter.addWidget(self.staff_view)


        hbox = QHBoxLayout(self)
        #hbox.addWidget(self.orgs_view)
        hbox.addWidget(splitter)
        self.setLayout(hbox)


    @pyqtSlot(QModelIndex)
    def org_view_changed(self, current: QModelIndex):
        self.orgs_view.model.get_children(current)
        #self.staff_view.model.refresh
        org = current.data(Qt.ItemDataRole.UserRole+0)
        print(org)

