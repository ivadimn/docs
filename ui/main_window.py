from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication, QTabWidget
from PyQt6.QtCore import pyqtSlot, Qt
from ui.main_menu import MainMenu
from load_data.load_orgs import LoadOrgs
from load_data.load_simple import LoadSimple
from load_data.load_faces import LoadFaces
from load_data.import_data import ImportData
from ui.views.orgs_view import OrgsView
from ui.views.group_view import GroupView
from ui.widgets.groups_widget import GroupsWidget
from repositories.org_repository import TreeRepository


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

        main_menu.groups.triggered.connect(self.nsi_groups)

        main_menu.orgs.triggered.connect(self.load_orgs)
        main_menu.deps.triggered.connect(self.load_simple)
        main_menu.faces.triggered.connect(self.load_faces)

        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)

        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab)

    @pyqtSlot()
    def nsi_groups(self):
        #view = GroupView(self)
        widget = GroupsWidget(self)
        self.tab.addTab(widget, "Группы должностей")

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
        view = OrgsView(parent=self)
        self.tab.addTab(view, "Структура")

    @pyqtSlot()
    def load_simple(self):
        file_dlg = QFileDialog(self, Qt.WindowType.Dialog)
        file_dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dlg.setNameFilter("Excel files (*.xls *.xlsx)")
        if not file_dlg.exec():
            return
        file_name = file_dlg.selectedFiles()[0]
        file_dlg.close()
        # load = LoadSimple(file_name)
        # load.update_db_deps()
        load = ImportData(file_name)

    @pyqtSlot()
    def load_faces(self):
        file_dlg = QFileDialog(self, Qt.WindowType.Dialog)
        file_dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dlg.setNameFilter("Excel files (*.xls *.xlsx)")
        if not file_dlg.exec():
            return
        file_name = file_dlg.selectedFiles()[0]
        load = LoadFaces(file_name)
        load.update_db_faces()

    @pyqtSlot()
    def close_tab(self):
        index = self.tab.currentIndex()
        print(index)
        self.tab.removeTab(index)
