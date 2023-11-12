import typing
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSlot
from PyQt6.QtSql import QSqlQuery
from model_data.group_position import GroupPosition

import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class GroupModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._labels = ["Наименование группы", "Уровень", ""]
        self._groups = list()
        self.refresh()

    def rowCount(self, parent_index: QModelIndex = ...) -> int:
        if parent_index.isValid():
            return 0
        return len(self._groups)

    def columnCount(self, parent_index: QModelIndex = ...) -> int:
        return 0 if parent_index.isValid() else 2

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        r = index.row()
        c = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            if c == 0:
                return self._groups[r].name
            elif c == 1:
                return self._groups[r].level
            else:
                return f"{r=}, {c=}"
        elif role == Qt.ItemDataRole.UserRole+0:
            return self._groups[r]
        else:
            return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self._labels[section]
        elif role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        else:
            return None

    def refresh(self):
        self.beginResetModel()
        try:
            self._groups = GroupPosition.select()
        finally:
            self.endResetModel()
