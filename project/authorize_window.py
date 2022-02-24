from ui_authorize_window import *
from registration_window import *
from main_window import *
from PyQt5.QtCore import QSettings


class AuthorizeWindow(QtWidgets.QWidget):
    def __init__(self):
        super(AuthorizeWindow, self).__init__()

        self.__ui = Ui_AuthorizeWindow()
        self.__ui.setupUi(self)
        self.setFixedSize(290, 210)

        self.__main_window = None
        self.__registration_window = RegistrationWindow(self)

        self.__ui.button_registration.clicked.connect(self._on_button_registration)
        self.__ui.button_login.clicked.connect(self._on_button_login)
        self.__ui.button_cancel.clicked.connect(self._on_button_cancel)
        self.__ui.check_box_show_pasword.clicked.connect(self._on_check_box_show_password)

        self._on_check_box_show_password(False)

        file_handler = logging.FileHandler('authorize.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.addHandler(file_handler)

        self.__settings = QSettings('settings.ini', QSettings.IniFormat)
        self.__ui.line_edit_username.setText(self.__settings.value('auth/username'))
        self.__ui.line_edit_password.setText(self.__settings.value('auth/password'))

    def _on_button_registration(self):
        self.__registration_window.show()
        self.close()

    def _on_button_login(self):
        username = self.__ui.line_edit_username.text()
        password = self.__ui.line_edit_password.text()

        self.__logger.debug('login - {}'.format(username))

        if self.__ui.check_box_remember.isChecked():
            self.__settings.setValue('auth/username', username)
            self.__settings.setValue('auth/password', password)

        self.__main_window = MainWindow(username)
        self.__main_window.show()
        self.close()

    def _on_button_cancel(self):
        self.close()

    def _on_check_box_show_password(self, checked):
        if checked:
            self.__ui.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.__ui.line_edit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
