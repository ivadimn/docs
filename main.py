import sys
from application import Application
from ui.main_window import MainWindow
from db.connection import Connection
import logging


if __name__ == '__main__':
    #logging.basicConfig(encoding="utf-8", level=logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)
    app = Application(sys.argv)
    main_window = MainWindow()
    main_window.show()
    conn1 = Connection()
    sys.exit(app.exec())

