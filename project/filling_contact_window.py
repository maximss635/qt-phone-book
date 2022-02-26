from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QValidator, QRegExpValidator

from ui_filling_contact_window import *


class FillingContactWindow(QtWidgets.QDialog):
    def __init__(self, name=None, phone=None, birthday=None):
        super(FillingContactWindow, self).__init__()

        self.__ui = Ui_FillingContactWindow()
        self.__ui.setupUi(self)
        self.setFixedSize(370, 210)
        self.setWindowTitle('Заполнение контакта')

        expr = QRegExp("(19[0-9][0-9]|20[0-9][0-9])-(0[1-9]|[1][0-2])-(0[1-9]|[12][0-9]|3[01])")
        validator = QRegExpValidator(expr, self)
        self.__ui.line_edit_birthday.setValidator(validator)

        expr = QRegExp('(8|\+7)([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])')
        validator = QRegExpValidator(expr, self)
        self.__ui.line_edit_phone.setValidator(validator)

        expr = QRegExp('([а-я]|[А-Я]|\s)*')
        validator = QRegExpValidator(expr, self)
        self.__ui.line_edit_name.setValidator(validator)
        self.__ui.line_edit_name.setMaxLength(50)

        self.__ui.line_edit_name.setText(name)
        self.__ui.line_edit_phone.setText(phone)
        self.__ui.line_edit_birthday.setText(birthday)

    def get_object(self):
        return (self.__ui.line_edit_name.text(),
                self.__ui.line_edit_phone.text(),
                self.__ui.line_edit_birthday.text())

    def accept(self):
        if not self.__ui.line_edit_name.hasAcceptableInput() or \
                not self.__ui.line_edit_phone.hasAcceptableInput() or \
                not self.__ui.line_edit_birthday.hasAcceptableInput():
            self.__ui.label_info.setText('Ошибка заполнения')
            return None

        return super(FillingContactWindow, self).accept()
