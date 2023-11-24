import typing
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSlot
from model_data.position import Position


class PositionTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__poss = list()
        self._hlabels = ["Наименование должности", "Уровень", ]
        self.refresh()

    def refresh(self):
        self.beginResetModel()
        try:
            self.__poss.clear()
            self.__poss = Position.select()
        finally:
            self.endResetModel()

    def rowCount(self, parent_index: QModelIndex = ...) -> int:
        if parent_index.isValid():
            return 0
        return len(self.__poss)

    def columnCount(self, parent_index: QModelIndex = ...) -> int:
        return 0 if parent_index.isValid() else 2

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._hlabels[section]
        elif role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        else:
            return None

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        r = index.row()
        c = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            if c == 0:
                return self.__poss[r].name
            elif c == 1:
                return self.__poss[r].group_name
            else:
                return f"{r=}, {c=}"
        else:
            return None
