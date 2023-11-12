from PyQt6.QtCore import Qt
from .view import View
from models.group_model import GroupModel
from dialogs.group_dialog import GroupDialog
from model_data.group_position import GroupPosition


class GroupView(View):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = GroupModel()
        self.setModel(self.model)

        hh = self.horizontalHeader()
        hh.setSectionResizeMode(1, hh.ResizeMode.Stretch)

    def add(self) -> None:
        dlg = GroupDialog(self)
        dlg.level = 0
        if dlg.exec():
            group = GroupPosition()
            dlg.get(group)
            group.save()
            self.model.refresh()

    def update(self) -> None:
        dlg = GroupDialog(self)
        index = self.currentIndex()
        grp = self.model.data(index, Qt.ItemDataRole.UserRole + 0)
        grp = GroupPosition(pk=grp.pk).load()
        dlg.put(grp)
        if dlg.exec():
            dlg.get(grp)
            grp.save()
            self.model.refresh()

    def delete(self) -> None:
        pass
