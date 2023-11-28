from PyQt6.QtWidgets import QDialog, QFrame, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from model_data.group_position import GroupPosition
from model_data.position import Position
from models.group_list_model import GroupListModel
from .position_form import Ui_PositionForm


class _Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_PositionForm()
        self.ui.setupUi(self)


class PositionDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Должность")

        self.__frame = _Frame(parent=self)
        #self.__model = GroupListModel()

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
        self.__init_levels()

    @property
    def cbx(self):
        return self.__frame.ui.cbx_level

    @property
    def group_id(self):
        grp = self.cbx.currentData()
        if grp:
            return grp.pk
        return None

    @property
    def name(self):
        result = self.__frame.ui.edt_name.text().strip()
        return None if result == "" else result

    @name.setter
    def name(self, value: str):
        self.__frame.ui.edt_name.setText(value)

    def get(self, pos: Position):
        pos.name = self.name
        pos.group_id = self.group_id

    def put(self, pos: Position):
        self.name = pos.name
        if pos.group_id:
            grp = GroupPosition(pk=pos.group_id).load()
            index = self.cbx.findText(grp.name)
            if index > 0:
                self.cbx.setCurrentIndex(index)

    def __init_levels(self):
        groups = GroupPosition.select()
        self.__frame.ui.cbx_level.addItem("Не указано", None)
        for g in groups:
            self.__frame.ui.cbx_level.addItem(g.name, g)

    def finish(self):
        if self.group_id is None:
            return
        self.accept()
