from PyQt6.QtWidgets import QMenuBar


class MainMenu(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)

        nsi_menu = self.addMenu("НСИ")
        self.__pd = nsi_menu.addAction("Персональные данных")
        self.__goals = nsi_menu.addAction("Цели обработки ПД")
        self.__category = nsi_menu.addAction("Категории субъектов ПД")

        help_menu = self.addMenu("Справка")
        self.__about = help_menu.addAction("О программе...")
        self.__about_qt = help_menu.addAction("О библиотеке Qt...")

    @property
    def about(self):
        return self.__about

    @property
    def about_qt(self):
        return self.__about_qt
