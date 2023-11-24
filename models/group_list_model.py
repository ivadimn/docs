import typing
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex
from model_data.group_position import GroupPosition


class GroupListModel(QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__groups = list()

    def rowCount(self, parent_index: QModelIndex = ...) -> int:
        if parent_index.isValid():
            return 0
        return len(self.__groups)

    def columnCount(self, parent_index: QModelIndex = ...) -> int:
        if parent_index.isValid():
            return 0
        return 1

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.__groups[index.row()].name
        return None

    def refresh(self):
        self.__groups = GroupPosition.select()
