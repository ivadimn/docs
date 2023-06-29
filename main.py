import sys
from application import Application
from ui.main_window import MainWindow
from db.connection import Connection
from repositories.pd_repository import PdRepository
from model_data.pd import Pd

if __name__ == '__main__':
    app = Application(sys.argv)
    main_window = MainWindow()
    main_window.show()
    conn = Connection()


    sys.exit(app.exec())
