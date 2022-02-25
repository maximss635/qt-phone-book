from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QValidator, QRegExpValidator

from ui_adding_contact_window import *


class AddingContactWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AddingContactWindow, self).__init__()

        self.__ui = Ui_AddingContactWindow()
        self.__ui.setupUi(self)
        self.setFixedSize(290, 210)

        expr = QRegExp("(0[1-9]|[12][0-9]|3[01])-(0[1-9]|[1][0-2])-(19[0-9][0-9]|20[0-9][0-9])")
        validator = QRegExpValidator(expr, self)
        self.__ui.line_edit_birthday.setValidator(validator)

        expr = QRegExp('(8|\+7)([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])')
        validator = QRegExpValidator(expr, self)
        self.__ui.line_edit_phone.setValidator(validator)

    def get_object(self):
        return (self.__ui.line_edit_name.text(),
                self.__ui.line_edit_phone.text(),
                self.__ui.line_edit_birthday.text())
