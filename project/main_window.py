from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QTableWidgetItem
from datetime import datetime
import mariadb
import logging

from ui_main_window import *
from registration_window import *
from authorize_window import *
from reset_password_window import *
from adding_contact_window import *


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
        self.__ui.check_box_show_all.clicked.connect(self._on_check_box_show_all)

        # Logger
        file_handler = logging.FileHandler('{}.log'.format(datetime.now().date().__str__()))
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

        last_username = self.settings.value('app-auth/username')
        last_password = self.settings.value('app-auth/password')
        if (last_username is not None) and (last_password is not None):
            self.login(last_username, last_password)

    def show(self):
        if self.__current_user is not None:
            self.__ui.label_hello.setText('Вы вошли, как {}'.format(self.__current_user[1]))
            self._load_table('А')
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

        cur.close()

        return self.__current_user

    def logout(self):
        self.__current_user = None
        self.settings.remove('app-auth/username')
        self.settings.remove('app-auth/password')
        self.close()
        self.__authorize_window.show()

    def _on_navigation_panel_clicked(self, index):
        self.__ui.check_box_show_all.setChecked(False)
        letter = index.data()
        self._load_table(letter)

    def _on_button_add(self):
        adding_contact_window = AddingContactWindow()

        self.setEnabled(False)
        exit_code = adding_contact_window.exec()
        self.setEnabled(True)

        if exit_code != 0:
            name, phone, birthday = adding_contact_window.get_object()
            self._add_contact_to_db(name, phone, birthday)

    def _on_check_box_show_all(self, checked):
        if checked:
            self._load_table(letter=None)
        else:
            selected_indexes = self.__ui.navigation_panel.selectedIndexes()
            if len(selected_indexes) > 0:
                self._load_table(selected_indexes[0].data())
            else:
                self._load_table('А')

    def _load_table(self, letter):
        self.__logger.debug('load table \'{}\''.format(letter if letter is not None else 'all'))

        cur = self.__db.cursor()
        current_user_id = self.__current_user[0]

        if letter is not None:
            cur.execute('SELECT name, phone, birthday FROM Contacts'
                        ' WHERE owner_id = \'{}\' AND name LIKE \'{}%\';'.format(
                            current_user_id, letter))
        else:
            cur.execute('SELECT name, phone, birthday FROM Contacts'
                        ' WHERE owner_id = \'{}\';'.format(
                            current_user_id))

        table_model = cur.fetchall()
        self.__ui.table_contacts.setRowCount(len(table_model))

        for row, (name, phone, birthday) in enumerate(table_model):
            self.__ui.table_contacts.setItem(row, 0, QTableWidgetItem(name))
            self.__ui.table_contacts.setItem(row, 1, QTableWidgetItem(phone))
            self.__ui.table_contacts.setItem(row, 2, QTableWidgetItem(birthday.__str__()))

        cur.close()

    def _add_contact_to_db(self, name, phone, birthday):
        cur = self.__db.cursor()
        current_user_id = self.__current_user[0]

        cur.execute('INSERT INTO Contacts (name, phone, birthday, owner_id) values ' \
            '(\'{}\', \'{}\', \'{}\', \'{}\');'.format(
                name, phone, birthday, current_user_id
        ))

        cur.close()
        self.__db.commit()

        self.__logger.debug('new contact - {}'.format(name))
