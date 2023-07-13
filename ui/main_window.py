from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication
from PyQt6.QtCore import pyqtSlot, Qt
from ui.main_menu import MainMenu
from load_data.load import load_deps


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
            load_deps(file_name)


