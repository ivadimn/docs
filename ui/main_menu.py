from PyQt6.QtWidgets import QMenuBar


class MainMenu(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        nsi_menu = self.addMenu("НСИ")
        self.__groups = nsi_menu.addAction("Группы должностей ...")
        self.__positions = nsi_menu.addAction("Должности ...")
        self.__category = nsi_menu.addAction("Категории субъектов ПД")

        load_menu = self.addMenu("Загрузка данных")
        self.__orgs = load_menu.addAction("Организационные единицы ...")
        self.__deps = load_menu.addAction("Департаменты ...")
        self.__faces = load_menu.addAction("Лица ...")
        self.__tn = load_menu.addAction("Табельные номера ...")

        help_menu = self.addMenu("Справка")
        self.__about = help_menu.addAction("О программе...")
        self.__about_qt = help_menu.addAction("О библиотеке Qt...")

    @property
    def groups(self):
        return self.__groups

    @property
    def positions(self):
        return self.__positions

    @property
    def orgs(self):
        return self.__orgs

    @property
    def deps(self):
        return self.__deps

    @property
    def faces(self):
        return self.__faces

    @property
    def tn(self):
        return self.__tn

    @property
    def about(self):
        return self.__about

    @property
    def about_qt(self):
        return self.__about_qt
