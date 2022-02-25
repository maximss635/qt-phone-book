from PyQt5.QtWidgets import QApplication
from sys import argv

from main_window import *


def main():
    app = QApplication(argv)

    main_window = MainWindow()
    main_window.show()

    return app.exec()


if __name__ == '__main__':
    main()
    