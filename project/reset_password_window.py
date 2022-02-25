from ui_reset_password_window import *


class ResetPasswordWindow(QtWidgets.QWidget):
    def __init__(self, authorized_window, db=False):
        super(ResetPasswordWindow, self).__init__()

        self.__authorized_window = authorized_window

        self.__ui = Ui_ResetPasswordWindow()
        self.__ui.setupUi(self)
        self.setFixedSize(290, 210)

        self.__ui.button_change_password.clicked.connect(self._on_button_change_password)
        self.__ui.button_cancel.clicked.connect(self._on_button_cancel)

    def _on_button_change_password(self):
        # TODO - ???
        pass

    def _on_button_cancel(self):
        self.__authorized_window.show()
        self.close()
