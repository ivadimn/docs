from PyQt6.QtWidgets import QTableView


class StaffView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

    def refresh(self):
        pass
