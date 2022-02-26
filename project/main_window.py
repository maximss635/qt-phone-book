from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QTableWidgetItem
from datetime import datetime
import mariadb
import logging

from ui_main_window import *
from authorize_window import *
from registration_window import *
from reset_password_window import *
from filling_contact_window import *


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
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def _db_read_contacts(self, letter, view):
        cur = self._db.cursor()
        current_user_id = self._current_user[0]

        contacts_all = None
        if letter is not None:
            query = 'SELECT id, name, phone, birthday '\
                    'FROM Contacts ' \
                    'WHERE owner_id = \'{}\' AND name LIKE \'{}%\';'.format(current_user_id, letter)

            self.logger.debug(query)
            cur.execute(query)

            table_model = cur.fetchall()

            query = 'SELECT COUNT(*) AS count FROM Contacts WHERE owner_id = {};'.format(
                current_user_id
            )

            self.logger.debug(query)
            cur.execute(query)
            contacts_all = int(cur.fetchone()[0])
        else:
            query = 'SELECT id, name, phone, birthday FROM Contacts'\
                    ' WHERE owner_id = \'{}\';'.format(
                        current_user_id)

            self.logger.debug(query)
            cur.execute(query)

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

    def _db_add_contact(self, name, phone, birthday):
        cur = self._db.cursor()
        current_user_id = self._current_user[0]

        query = 'INSERT INTO Contacts (name, phone, birthday, owner_id) values ' \
            '(\'{}\', \'{}\', \'{}\', \'{}\');'.format(
                name, phone, birthday, current_user_id)

        self.logger.debug(query)

        cur.execute(query)

        cur.close()
        self._db.commit()

    def _db_remove_contact(self, ids):
        cur = self._db.cursor()
        current_user_id = self._current_user[0]

        query = 'DELETE FROM Contacts '\
                'WHERE owner_id = {} AND id IN ('.format(current_user_id)

        for id in ids:
            query += '{}, '.format(id)
        query = query[:-2] + ');'

        self.logger.debug(query)
        cur.execute(query)

        cur.close()
        self._db.commit()

    def _db_update_contact(self, id, name, phone, birthday):
        cur = self._db.cursor()
        current_user_id = self._current_user[0]

        query = 'UPDATE Contacts '\
                'SET phone=\'{}\', birthday=\'{}\', name=\'{}\' '\
                'WHERE id={} and owner_id={};'.format(phone, birthday, name, id, current_user_id)

        self.logger.debug(query)
        cur.execute(query)

        cur.close()
        self._db.commit()

    def _db_check_birthday_people(self):
        cur = self._db.cursor()
        current_user_id = self._current_user[0]

        query = 'SELECT name '\
                'FROM Contacts '\
                'WHERE owner_id={} AND '\
                'DATE_FORMAT(birthday, \'%m-%d\') >= DATE_FORMAT(CURDATE(), \'%m-%d\') AND '\
                'DATE_FORMAT(birthday, \'%m-%d\') < DATE_FORMAT(CURDATE() + INTERVAL 7 DAY, \'%m-%d\');'\
            .format(current_user_id)

        self.logger.debug(query)
        cur.execute(query)

        results = cur.fetchall()
        cur.close()

        return results


class MainWindow(QtWidgets.QMainWindow, DBConnection):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.setWindowTitle('Главное окно')

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
        self.__ui.button_update.setEnabled(False)
        self.__ui.table_contacts.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

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
        self.__ui.button_update.clicked.connect(self._on_button_update)
        self.__ui.table_contacts.cellDoubleClicked.connect(self._on_button_update)

        last_username = self.settings.value('app-auth/username')
        last_password_hash = self.settings.value('app-auth/sha256-password')
        if (last_username is not None) and (last_password_hash is not None):
            self.login(last_username, last_password_hash)

    def show(self):
        if self._current_user is not None:
            self.__ui.label_hello.setText('Вы вошли, как {}'.format(self._current_user[1]))
            self._db_read_contacts('А', self.__ui)
            self.__ui.navigation_panel.item(0).setSelected(True)

            super(MainWindow, self).show()

            if self._current_user is not None:
                self._check_birthday_people()
        else:
            self.__authorize_window.show()

    def login(self, username, sha256_password, window=None):
        cur = self._db.cursor()
        username = username.replace('\'', '\\\'')

        query = 'SELECT * '\
                'FROM Users '\
                'WHERE username=\'{}\' AND sha256_password=\'{}\';'.format(username, sha256_password)

        self.logger.debug(query)

        cur.execute(query)

        self._current_user = cur.fetchone()
        if self._current_user is None:
            QtWidgets.QMessageBox.information(window, 'Ошибка',
                                              'Пользователь с такими данными не найден',
                                              QtWidgets.QMessageBox.Ok)
            return None

        cur.close()

        return self._current_user

    def logout(self):
        self._current_user = None
        self.settings.remove('app-auth/username')
        self.settings.remove('app-auth/sha256-password')
        self.close()
        self.__authorize_window.show()

    def _on_navigation_panel_clicked(self, index):
        self.__ui.check_box_show_all.setChecked(False)
        letter = index.data()
        self._db_read_contacts(letter, self.__ui)

    def _on_check_box_show_all(self, checked):
        if checked:
            self._db_read_contacts(None, self.__ui)
            for item in self.__ui.navigation_panel.selectedItems():
                item.setSelected(False)
        else:
            self._db_read_contacts('А', self.__ui)
            self.__ui.navigation_panel.item(0).setSelected(True)

    def _on_contact_clicked(self, row, column):
        self.__ui.button_delete.setEnabled(True)
        self.__ui.button_update.setEnabled(True)

    def __get_ids_of_selected_contacts(self):
        ids = set()
        selected_indexes = self.__ui.table_contacts.selectedIndexes()
        for index in selected_indexes:
            row = index.row()
            ids.add(int(self.__ui.table_contacts.item(row, 3).text()))  # hidden column with ids

        return ids

    def _on_button_add(self):
        filling_contact_window = FillingContactWindow()

        self.setEnabled(False)
        exit_code = filling_contact_window.exec()
        self.setEnabled(True)

        if exit_code != 0:
            name, phone, birthday = filling_contact_window.get_object()
            self._db_add_contact(name, phone, birthday)

            # Update in view
            self._db_read_contacts(name[0], self.__ui)
            self.__ui.check_box_show_all.setChecked(False)
            for i in range(self.__ui.navigation_panel.count()):
                item = self.__ui.navigation_panel.item(i)
                if item.text() == name[0] or item.text() == name[0].upper():
                    item.setSelected(True)
                    break

    def _on_button_delete(self):
        selected_indexes = self.__ui.table_contacts.selectedIndexes()
        if len(selected_indexes) == 0:
            self.__ui.button_delete.setEnabled(False)
            return

        ids_to_remove = self.__get_ids_of_selected_contacts()
        buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        answer = QtWidgets.QMessageBox.question(self, 'Подтвердите действие',
                                              'Вы уверены, что хотите удалить {} контактов?'.format(len(ids_to_remove)),
                                              buttons)

        if answer == QtWidgets.QMessageBox.No:
            return

        self._db_remove_contact(ids_to_remove)

        # Update in view
        if self.__ui.check_box_show_all.isChecked():
            self._db_read_contacts(None, self.__ui)
        else:
            selected_items = self.__ui.navigation_panel.selectedItems()
            self._db_read_contacts(selected_items[0].text(), self.__ui)

    def _on_button_update(self):
        selected_indexes = self.__ui.table_contacts.selectedIndexes()
        if len(selected_indexes) == 0:
            self.__ui.button_update.setEnabled(False)
            return

        ids_to_update = self.__get_ids_of_selected_contacts()
        if len(ids_to_update) != 1:
            QtWidgets.QMessageBox.information(self, 'Ошибка', 'Пожалуйста, выделите одну строчку для редактирования')
            return

        row = selected_indexes[0].row()

        name = self.__ui.table_contacts.item(row, 0).text()
        phone = self.__ui.table_contacts.item(row, 1).text()
        birthday = self.__ui.table_contacts.item(row, 2).text()
        id = int(self.__ui.table_contacts.item(row, 3).text())

        filling_contact_window = FillingContactWindow(name, phone, birthday)

        self.setEnabled(False)
        exit_code = filling_contact_window.exec()
        self.setEnabled(True)

        if exit_code != 0:
            name, phone, birthday = filling_contact_window.get_object()
            self._db_update_contact(id, name, phone, birthday)

            # Update in view
            if self.__ui.check_box_show_all.isChecked():
                self._db_read_contacts(None, self.__ui)
            else:
                selected_items = self.__ui.navigation_panel.selectedItems()
                self._db_read_contacts(selected_items[0].text(), self.__ui)

    def _check_birthday_people(self):
        birthday_people = self._db_check_birthday_people()

        if len(birthday_people) > 0:
            QtWidgets.QMessageBox.information(self, 'Напоминание',
                                              'В ближайшую неделю дни рождения у: {}'.format(birthday_people))
