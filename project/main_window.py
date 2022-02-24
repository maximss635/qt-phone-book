from ui_main_window import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, username, authorized_window):
        super(MainWindow, self).__init__()

        self.__authorized_window = authorized_window
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(self.__ui.main_layout)
        self.setCentralWidget(central_widget)
        self.__ui.navigation_panel.setFixedWidth(100)

        self.__ui.label_hello.setText('Вы вошли, как {}'.format(username))

        self.__ui.button_add.clicked.connect(self._on_button_add)
        self.__ui.navigation_panel.clicked.connect(self._on_navigation_panel_clicked)
        self.__ui.button_logout.clicked.connect(self._on_button_logout)

    def _on_navigation_panel_clicked(self, index):
        print(index.data())

        # Из data берем буквы
        # По ним делаем запросы в БД
        # Отображаем в self.__ui.main_table

    def _on_button_add(self):
        pass
        # TODO: Not implemented yet

    def _on_button_logout(self):
        self.__authorized_window.show()
        self.close()
