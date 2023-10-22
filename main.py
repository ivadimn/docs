import sys
from application import Application
from ui.main_window import MainWindow
from db.connection import Connection
import logging


if __name__ == '__main__':
    logging.basicConfig(encoding="utf-8", level=logging.WARNING)
    app = Application(sys.argv)
    main_window = MainWindow()
    main_window.show()
    conn = Connection()
    sys.exit(app.exec())

