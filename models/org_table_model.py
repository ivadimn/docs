import typing
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSlot
from model_data.staff import Staff


class OrgTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__staffs = list()
        self.__org_id = None
        self._hlabels = ["Табельный №", "ФИО", "Должность", ]
        self.refresh()

    @property
    def org(self):
        return self.__org_id

    def rowCount(self, parent_index: QModelIndex = ...) -> int:
        if parent_index.isValid():
            return 0
        return len(self.__staffs)

    def columnCount(self, parent_index: QModelIndex = ...) -> int:
        return 0 if parent_index.isValid() else 3

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation != Qt.Orientation.Horizontal or role != Qt.ItemDataRole.DisplayRole:
            return None
        return self._hlabels[section]

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        r = index.row()
        c = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            if c == 0:
                return self.__staffs[r].tn
            elif c == 1:
                return "{0} {1} {2}".format(self.__staffs[r].firstname, self.__staffs[r].name,
                                            self.__staffs[r].fathername)
            elif c == 2:
                return self.__staffs[r].position
            else:
                return f"{r=}, {c=}"
        else:
            return None

    def refresh(self, org_id: int = None):
        self.beginResetModel()
        self.__org_id = org_id
        try:
            self.__staffs.clear()
            if org_id is None:
                self.endResetModel()
                return
            self.__get_staffs(org_id)
        finally:
            self.endResetModel()

    def __get_staffs(self, org_id: int):
        self.__staffs = Staff.select_staffs(org_id)

