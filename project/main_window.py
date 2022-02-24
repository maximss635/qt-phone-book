from ui_main_window import *


from PyQt5.QtCore import QModelIndex

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super(MainWindow, self).__init__()

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__ui.pushButton.setText('Hello, {}!'.format(username))

        self.__ui.navigation_panel.clicked.connect(self._on_navigation_panel_clicked)

    def _on_navigation_panel_clicked(self, index):
        print(index.data())

        # Из data берем буквы
        # По ним делаем запросы в БД
        # Отображаем в self.__ui.main_table
