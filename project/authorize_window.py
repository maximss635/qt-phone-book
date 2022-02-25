from ui_authorize_window import *


class AuthorizeWindow(QtWidgets.QWidget):
    def __init__(self, main_window, registration_window, reset_password_window):
        super(AuthorizeWindow, self).__init__()

        self.__main_window = main_window
        self.__registration_window = registration_window
        self.__reset_password_window = reset_password_window

        self.__ui = Ui_AuthorizeWindow()
        self.__ui.setupUi(self)
        self.setFixedSize(290, 210)

        self.__ui.button_registration.clicked.connect(self._on_button_registration)
        self.__ui.button_login.clicked.connect(self._on_button_login)
        self.__ui.button_cancel.clicked.connect(self.close)
        self.__ui.button_reset_password.clicked.connect(self._on_button_reset_password)
        self.__ui.check_box_show_pasword.clicked.connect(self._on_check_box_show_password)

        self._on_check_box_show_password(False)

        self.__ui.line_edit_username.setText(main_window.settings.value('app-auth/username'))
        self.__ui.line_edit_password.setText(main_window.settings.value('app-auth/password'))

    def _on_button_login(self):
        username = self.__ui.line_edit_username.text()
        password = self.__ui.line_edit_password.text()

        user_model = self.__main_window.login(username, password, self)
        if (user_model is not None) and self.__ui.check_box_remember.isChecked():
            self.__main_window.settings.setValue('app-auth/username', user_model[1])
            self.__main_window.settings.setValue('app-auth/password', user_model[2])

        self.close()
        self.__main_window.show()

    def _on_button_reset_password(self):
        self.__reset_password_window.show()
        self.close()

    def _on_button_registration(self):
        self.__registration_window.show()
        self.close()

    def _on_check_box_show_password(self, checked):
        if checked:
            self.__ui.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.__ui.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def closeEvent(self, event):
        self.__ui.line_edit_username.clear()
        self.__ui.line_edit_password.clear()
