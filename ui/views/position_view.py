from PyQt6.QtCore import Qt
from .view import View
from models.position_model import PositionTableModel
from dialogs.position_dialog import PositionDialog
from model_data.position import Position


class PositionView(View):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = PositionTableModel()
        self.setModel(self.__model)

        hh = self.horizontalHeader()
        hh.setSectionResizeMode(1, hh.ResizeMode.Stretch)

    def add(self) -> None:
        pass

    def update(self) -> None:
        dlg = PositionDialog(self)
        index = self.currentIndex()
        pos = self.__model.data(index, Qt.ItemDataRole.UserRole + 0)
        pos = Position(pk=pos.pk).load()
        dlg.put(pos)
        if dlg.exec():
            dlg.get(pos)
            pos.save()
            self.__model.refresh()

    def delete(self) -> None:
        pass


