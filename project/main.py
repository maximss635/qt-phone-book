from PyQt5.QtWidgets import QApplication
from authorize_window import *
from sys import argv


def main():
    app = QApplication(argv)

    authorized_window = AuthorizeWindow()
    authorized_window.show()

    return app.exec()


if __name__ == '__main__':
    main()
    