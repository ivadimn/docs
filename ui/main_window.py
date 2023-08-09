from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication
from PyQt6.QtCore import pyqtSlot, Qt
from ui.main_menu import MainMenu
from load_data.load_orgs import LoadOrgs
from load_data.load_simple import LoadSimple
from repositories.org_repository import TreeRepository


data = [
('Вина', 0, 0),
('Белые сорта вин', 1, 1),
('Французские белые вина', 2, 2),
('Chardonnay', 3, 3),
('Colombard', 4, 3),
('Folle blanche', 5, 3),
('Ugni blanc', 6, 3),
('Muscadelle', 7, 3),
('Chenin', 8, 3),
('Итальянские белые вина', 9, 2),
('Castelli Romani Bianco', 10, 3),
('Tusculum Bianco', 11, 3),
('Красные сорта вин', 12, 1),
('Французкие красные вина', 13, 2),
('Cabernet', 14, 3),
('Franc', 15, 4),
('Sauvignon', 16, 4),
('Carmenere', 17, 3),
('Beaujolais nouveau', 18, 3),
('Итальянские красные вина', 19, 2),
('Bardolino', 20, 3),
('Syrah Cabernet', 21, 3),
('Castelli Romani Rosso', 22, 3),
]


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        screen = QApplication.screens()[0]
        width, height = screen.size().width(), screen.size().height()
        x = width // 4
        y = height // 4
        self.setGeometry(x, y, x * 2, y * 2)

        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)

        main_menu.orgs.triggered.connect(self.load_orgs)
        main_menu.deps.triggered.connect(self.load_simple)

        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)

    def about(self):
        title = "Цифровые нормативные документы"
        text = ("Программа для создания\n" +
                "цифровых нормативных документов.")
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, "Цифровые нормативные документы")

    @pyqtSlot()
    def load_orgs(self):
        file_dlg = QFileDialog(self, Qt.WindowType.Dialog)
        file_dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dlg.setNameFilter("Excel files (*.xls *.xlsx)")
        if file_dlg.exec():
            file_name = file_dlg.selectedFiles()[0]
            load = LoadOrgs(file_name)
            load.load_orgs()

    @pyqtSlot()
    def load_simple(self):
        file_dlg = QFileDialog(self, Qt.WindowType.Dialog)
        file_dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dlg.setNameFilter("Excel files (*.xls *.xlsx)")
        if file_dlg.exec():
            file_name = file_dlg.selectedFiles()[0]
            load = LoadSimple(file_name)
            load.update_db_deps()

