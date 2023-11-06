import sys
from application import Application
from ui.main_window import MainWindow
from db.db import Db
import logging


if __name__ == '__main__':
    #logging.basicConfig(encoding="utf-8", level=logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)
    app = Application(sys.argv)
    main_window = MainWindow()
    Db.init_connection()
    main_window.show()
    result = app.exec()
    Db.close_connection()
    sys.exit(result)

