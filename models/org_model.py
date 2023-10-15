from PyQt6.QtCore import QAbstractItemModel, QObject, QModelIndex, Qt
import typing


class OrgModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._columns = ("Код", "Наименование",)

        self._root_item = QObject(self)

    def add_item(self, item: QObject, parent_index: QModelIndex = None):
        self.beginInsertRows(parent_index, self.rowCount(parent_index), self.rowCount(parent_index))
        item.setParent(self.obj_by_index(parent_index))
        self.endInsertRows()

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parent_obj = self.obj_by_index(parent)
        return self.createIndex(row, column, parent_obj.children()[row])

    def parent(self, child: QModelIndex) -> QModelIndex:
        child_obj = self.obj_by_index(child)
        parent_obj = child_obj.parent()
        if parent_obj == self._root_item:
            return QModelIndex()
        grand_parent_obj = parent_obj.parent()
        row = grand_parent_obj.children().index(parent_obj)
        return self.createIndex(row, 0, parent_obj)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.obj_by_index(parent).children())

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self._columns)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return self.obj_by_index(index).property(self._columns[index.column()].encode("utf8"))
        return None

    def obj_by_index(self, index: QModelIndex) -> QObject:
        if index is None or not index.isValid():
            return self._root_item
        return index.internalPointer()
