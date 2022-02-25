from ui_registration_window import *


class RegistrationWindow(QtWidgets.QWidget):
    def __init__(self, authorize_window, db):
        super(RegistrationWindow, self).__init__()

        self.__db = db
        self.__authorize_window = authorize_window
        self.__ui = Ui_RegistrationWindow()
        self.__ui.setupUi(self)

        self.setFixedSize(290, 210)

        self.__ui.button_cancel.clicked.connect(self._on_button_cancel)
        self.__ui.button_registration.clicked.connect(self._on_button_registration)

    def _on_button_cancel(self):
        self._redirect_to_authorize()

    def _on_button_registration(self):
        username = self.__ui.line_edit_username.text()
        password = self.__ui.line_edit_password.text()
        password_2 = self.__ui.line_edit_password_2.text()
        birthday = self.__ui.line_edit_birthday.text()

        if password_2 != password:
            QtWidgets.QMessageBox.information(self, 'Error',
                                              'Пароли не совпадают',
                                              QtWidgets.QMessageBox.Ok)
            return

        cur = self.__db.cursor()
        cur.execute('SELECT id FROM Users WHERE username=\'{}\';'.format(
            username, password
        ))

        if cur.fetchone() is not None:
            QtWidgets.QMessageBox.information(self, 'Error',
                                              'Пользователь \'{}\' уже существует'.format(username),
                                              QtWidgets.QMessageBox.Ok)
            return

        cur.execute('INSERT INTO Users (username, password) VALUES (\'{}\', \'{}\');'.format(
            username, password
        ))

        self.__db.commit()
        self._redirect_to_authorize()

    def _redirect_to_authorize(self):
        self.__authorize_window.show()
        self.close()
