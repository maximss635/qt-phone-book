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


class DBConnection:
    def __init__(self):
        self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self._current_user = None

        self._db = mariadb.connect(
            database=self.settings.value('db-connection/database_name'),
            host=self.settings.value('db-connection/host'),
            user=self.settings.value('db-connection/user'),
            password=self.settings.value('db-connection/password'),
        )

        # Logger
        file_handler = logging.FileHandler('{}.log'.format(datetime.now().date().__str__()))
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)

    def _load_table(self, letter, view):
        self._logger.debug('load table \'{}\''.format(letter if letter is not None else 'all'))

        cur = self._db.cursor()
        current_user_id = self._current_user[0]

        contacts_all = None
        if letter is not None:
            cur.execute('SELECT id, name, phone, birthday FROM Contacts'
                        ' WHERE owner_id = \'{}\' AND name LIKE \'{}%\';'.format(
                            current_user_id, letter))

            table_model = cur.fetchall()

            cur.execute('SELECT COUNT(*) AS count FROM Contacts WHERE owner_id = {};'.format(
                current_user_id
            ))
            contacts_all = int(cur.fetchone()[0])
        else:
            cur.execute('SELECT id, name, phone, birthday FROM Contacts'
                        ' WHERE owner_id = \'{}\';'.format(
                            current_user_id))

            table_model = cur.fetchall()
            contacts_all = len(table_model)

        view.table_contacts.setRowCount(len(table_model))
        for row, (id, name, phone, birthday) in enumerate(table_model):
            view.table_contacts.setItem(row, 0, QTableWidgetItem(name))
            view.table_contacts.setItem(row, 1, QTableWidgetItem(phone))
            view.table_contacts.setItem(row, 2, QTableWidgetItem(birthday.__str__()))
            view.table_contacts.setItem(row, 3, QTableWidgetItem(str(id)))

        cur.close()

        view.label_status.setText('Всего: {}, Загружено: {}'.format(contacts_all, len(table_model)))

    def _add_contact_to_db(self, name, phone, birthday):
        cur = self._db.cursor()
        current_user_id = self._current_user[0]

        cur.execute('INSERT INTO Contacts (name, phone, birthday, owner_id) values ' \
            '(\'{}\', \'{}\', \'{}\', \'{}\');'.format(
                name, phone, birthday, current_user_id
        ))

        cur.close()
        self._db.commit()

        self._logger.debug('new contact - {}'.format(name))

    def _remove_contact_from_db(self, ids):
        cur = self._db.cursor()

        querry = 'DELETE FROM Contacts WHERE owner_id = 1 AND id IN ('
        for id in ids:
            querry += '{}, '.format(id)
        querry = querry[:-2] + ');'

        cur.execute(querry)

        cur.close()
        self._db.commit()

        self._logger.debug('delete contacts - {}'.format(ids))


class MainWindow(QtWidgets.QMainWindow, DBConnection):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        # Windows
        self.__registration_window = RegistrationWindow(self, self._db)
        self.__reset_password_window = ResetPasswordWindow(self)
        self.__authorize_window = AuthorizeWindow(self, self.__registration_window, self.__reset_password_window)

        # Pretty GUI
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(self.__ui.main_layout)
        self.setCentralWidget(central_widget)
        self.__ui.navigation_panel.setFixedWidth(100)
        self.__ui.button_delete.setEnabled(False)

        # do not show ids
        self.__ui.table_contacts.setColumnHidden(3, True)

        # Handlers
        self.__ui.button_add.clicked.connect(self._on_button_add)
        self.__ui.button_logout.clicked.connect(self.logout)
        self.__ui.navigation_panel.clicked.connect(self._on_navigation_panel_clicked)
        self.__ui.check_box_show_all.clicked.connect(self._on_check_box_show_all)
        self.__ui.table_contacts.cellClicked.connect(self._on_contact_clicked)
        self.__ui.table_contacts.cellEntered.connect(self._on_contact_clicked)
        self.__ui.button_delete.clicked.connect(self._on_button_delete)

        last_username = self.settings.value('app-auth/username')
        last_password = self.settings.value('app-auth/password')
        if (last_username is not None) and (last_password is not None):
            self.login(last_username, last_password)

    def show(self):
        if self._current_user is not None:
            self.__ui.label_hello.setText('Вы вошли, как {}'.format(self._current_user[1]))
            self._load_table('А', self.__ui)
            self.__ui.navigation_panel.item(0).setSelected(True)

            super(MainWindow, self).show()
        else:
            self.__authorize_window.show()

    def login(self, username, password, window=None):
        cur = self._db.cursor()
        cur.execute('SELECT * FROM Users WHERE username=\'{}\' AND password=\'{}\';'.format(
            username, password
        ))

        self._current_user = cur.fetchone()
        if self._current_user is None:
            QtWidgets.QMessageBox.information(window, 'Error',
                                              'Пользователь с такими данными не найден',
                                              QtWidgets.QMessageBox.Ok)
            return None

        self._logger.debug('login - {}'.format(username))

        cur.close()

        return self._current_user

    def logout(self):
        self._current_user = None
        self.settings.remove('app-auth/username')
        self.settings.remove('app-auth/password')
        self.close()
        self.__authorize_window.show()

    def _on_navigation_panel_clicked(self, index):
        self.__ui.check_box_show_all.setChecked(False)
        letter = index.data()
        self._load_table(letter, self.__ui)

    def _on_button_add(self):
        adding_contact_window = AddingContactWindow()

        self.setEnabled(False)
        exit_code = adding_contact_window.exec()
        self.setEnabled(True)

        if exit_code != 0:
            name, phone, birthday = adding_contact_window.get_object()
            self._add_contact_to_db(name, phone, birthday)
            self._load_table(name[0], self.__ui)

            self.__ui.check_box_show_all.setChecked(False)
            for i in range(self.__ui.navigation_panel.count()):
                item = self.__ui.navigation_panel.item(i)
                if item.text() == name[0] or item.text() == name[0].upper():
                    item.setSelected(True)
                    break

    def _on_check_box_show_all(self, checked):
        if checked:
            self._load_table(None, self.__ui)
            for item in self.__ui.navigation_panel.selectedItems():
                item.setSelected(False)
        else:
            self._load_table('А', self.__ui)
            self.__ui.navigation_panel.item(0).setSelected(True)

    def _on_contact_clicked(self, row, column):
        self.__ui.button_delete.setEnabled(True)

    def _on_button_delete(self):
        selected_indexes = self.__ui.table_contacts.selectedIndexes()
        if len(selected_indexes) == 0:
            self.__ui.button_delete.setEnabled(False)
            return

        ids_to_remove = set()
        for index in selected_indexes:
            row = index.row()
            ids_to_remove.add(int(self.__ui.table_contacts.item(row, 3).text()))

        self._remove_contact_from_db(ids_to_remove)

        if self.__ui.check_box_show_all.isChecked():
            self._load_table(None, self.__ui)
        else:
            selected_items = self.__ui.navigation_panel.selectedItems()
            self._load_table(selected_items[0].text(), self.__ui)
