from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSlot
from ui.views.position_view import PositionView


class PositionWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__view = PositionView(self)
        btn_update = QPushButton("Установить уровень должности", self)
        spacer = QSpacerItem(50, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        hbox = QHBoxLayout()
        hbox.addWidget(btn_update)
        hbox.addSpacerItem(spacer)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addWidget(self.__view)
        self.setLayout(vbox)

        btn_update.clicked.connect(self.update)

    @pyqtSlot()
    def update(self) -> None:
        self.__view.update()