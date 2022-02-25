from PyQt5.QtCore import QSettings
import mariadb
import logging

from ui_main_window import *
from registration_window import *
from authorize_window import *
from reset_password_window import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.__current_user = None
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.__db = mariadb.connect(
            database=self.settings.value('db-connection/database_name'),
            host=self.settings.value('db-connection/host'),
            user=self.settings.value('db-connection/user'),
            password=self.settings.value('db-connection/password'),
        )

        # Windows
        self.__registration_window = RegistrationWindow(self, self.__db)
        self.__reset_password_window = ResetPasswordWindow(self)
        self.__authorize_window = AuthorizeWindow(self, self.__registration_window, self.__reset_password_window)

        # Pretty GUI
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(self.__ui.main_layout)
        self.setCentralWidget(central_widget)
        self.__ui.navigation_panel.setFixedWidth(100)

        # Handlers
        self.__ui.button_add.clicked.connect(self._on_button_add)
        self.__ui.button_logout.clicked.connect(self.logout)
        self.__ui.navigation_panel.clicked.connect(self._on_navigation_panel_clicked)

        # Logger
        file_handler = logging.FileHandler('authorize.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.addHandler(file_handler)

        last_username = self.settings.value('app-auth/username')
        last_password = self.settings.value('app-auth/password')
        if (last_username is not None) and (last_password is not None):
            self.login(last_username, last_password)

    def show(self):
        if self.__current_user is not None:
            self.__ui.label_hello.setText('Вы вошли, как {}'.format(self.__current_user[1]))
            super(MainWindow, self).show()
        else:
            self.__authorize_window.show()

    def login(self, username, password, window=None):
        cur = self.__db.cursor()
        cur.execute('SELECT * FROM Users WHERE username=\'{}\' AND password=\'{}\';'.format(
            username, password
        ))

        self.__current_user = cur.fetchone()
        if self.__current_user is None:
            QtWidgets.QMessageBox.information(window, 'Error',
                                              'Пользователь с такими данными не найден',
                                              QtWidgets.QMessageBox.Ok)
            return None

        self.__logger.debug('login - {}'.format(username))

        return self.__current_user

    def logout(self):
        self.__current_user = None
        self.settings.remove('app-auth/username')
        self.settings.remove('app-auth/password')
        self.close()
        self.__authorize_window.show()

    def _on_navigation_panel_clicked(self, index):
        print(index.data())
        # TODO

        # Из data берем буквы
        # По ним делаем запросы в БД
        # Отображаем в self.__ui.main_table

    def _on_button_add(self):
        pass
        # TODO: Not implemented yet
