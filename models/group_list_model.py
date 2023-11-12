from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex


class GroupListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__groups = list()

    def rowCount(self, parent_index: QModelIndex = ...) -> int:
        if parent_index.isValid():
            return 0
        return len(self.__groups)

