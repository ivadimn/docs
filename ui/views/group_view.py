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
        dlg.level = 99
        if dlg.exec():
            group = GroupPosition()
            dlg.get(group)
            group.save()
            self.model.refresh()

    def update(self) -> None:
        pass

    def delete(self) -> None:
        pass
