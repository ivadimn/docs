from PyQt6.QtWidgets import QDialog, QFrame, QHBoxLayout, QPushButton, QVBoxLayout
from model_data.group_position import GroupPosition
from .group_form import Ui_GroupForm


class _Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_GroupForm()
        self.ui.setupUi(self)


class GroupDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Группа должностей")

        self.__frame = _Frame(parent=self)

        btn_ok = QPushButton("Ok", parent=self)
        btn_cancel = QPushButton("Отмена", parent=self)

        vbox = QVBoxLayout(self)

        vbox.addWidget(self.__frame)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(btn_ok)
        hbox.addWidget(btn_cancel)
        vbox.addLayout(hbox)

        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.finish)

    @property
    def name(self):
        result = self.__frame.ui.edt_name.text().strip()
        return None if result == "" else result

    @name.setter
    def name(self, value):
        self.__frame.ui.edt_name.setText(value)

    @property
    def level(self):
        return self.__frame.ui.spn_level.value()

    @level.setter
    def level(self, value: int):
        self.__frame.ui.spn_level.setValue(value)

    def finish(self):
        if self.name is None:
            return
        self.accept()

    def get(self, group: GroupPosition):
        group.name = self.name
        group.level = self.level

    def put(self, group: GroupPosition):
        self.name = group.name
        self.level = group.level
