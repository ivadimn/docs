from PyQt6.QtWidgets import QDialog, QFrame, QHBoxLayout, QPushButton, QVBoxLayout
from model_data.group_position import GroupPosition
from model_data.position import Position
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

    def __init_levels(self):
        groups = GroupPosition.select()
        self.__frame.ui.cbx_level.setModel()
        for g in groups:
            self.__frame.ui.cbx_level.addItem("{0}: {1}".format(g.name, g.level), g)

    def finish(self):
        pass