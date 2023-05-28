import sys
from application import Application
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = Application(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
