from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from Crypto.Hash import SHA256
from ui_registration_window import *


class RegistrationWindow(QtWidgets.QWidget):
    def __init__(self, authorize_window, db):
        super(RegistrationWindow, self).__init__()

        self.__db = db
        self.__authorize_window = authorize_window
        self.__ui = Ui_RegistrationWindow()
        self.__ui.setupUi(self)

        self.setFixedSize(290, 210)

        expr = QRegExp("(19[0-9][0-9]|20[0-9][0-9])-(0[1-9]|[1][0-2])-(0[1-9]|[12][0-9]|3[01])")
        validator = QRegExpValidator(expr, self)
        self.__ui.line_edit_birthday.setValidator(validator)

        self.__ui.button_cancel.clicked.connect(self._on_button_cancel)
        self.__ui.button_registration.clicked.connect(self._on_button_registration)

    def _on_button_cancel(self):
        self._redirect_to_authorize()

    def _on_button_registration(self):
        username = self.__ui.line_edit_username.text().replace('\'', '\\\'')
        password = self.__ui.line_edit_password.text()
        password_2 = self.__ui.line_edit_password_2.text()
        birthday = self.__ui.line_edit_birthday.text()

        if password_2 != password:
            QtWidgets.QMessageBox.information(self, 'Error',
                                              'Пароли не совпадают',
                                              QtWidgets.QMessageBox.Ok)
            return

        sha256_password = SHA256.new(bytes(password, encoding='utf-8')).hexdigest()

        cur = self.__db.cursor()
        query = 'SELECT id FROM Users WHERE username=\'{}\';'.format(
            username, sha256_password
        )

        self.__authorize_window.logger.debug(query)
        cur.execute(query)

        if cur.fetchone() is not None:
            QtWidgets.QMessageBox.information(self, 'Error',
                                              'Пользователь \'{}\' уже существует'.format(username),
                                              QtWidgets.QMessageBox.Ok)
            return

        query = 'INSERT INTO Users (username, sha256_password) VALUES (\'{}\', \'{}\');'.format(
            username, sha256_password
        )

        self.__authorize_window.logger.debug(query)
        cur.execute(query)

        cur.close()
        self.__db.commit()

        self._redirect_to_authorize()

    def _redirect_to_authorize(self):
        self.__authorize_window.show()
        self.close()
