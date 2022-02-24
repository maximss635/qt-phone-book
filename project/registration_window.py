from ui_registration_window import *
import logging


class RegistrationWindow(QtWidgets.QWidget):
    def __init__(self):
        super(RegistrationWindow, self).__init__()

        self.__ui = Ui_RegistrationWindow()
        self.__ui.setupUi(self)

        self.setFixedSize(290, 200)

        file_handler = logging.FileHandler('registrations.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.addHandler(file_handler)

        self.__ui.button_cancel.clicked.connect(self._on_button_cancel)
        self.__ui.button_registration.clicked.connect(self._on_button_registration)

    def _on_button_cancel(self):
        # Not implemented yet
        pass

    def _on_button_registration(self):
        # Not implemented yet
        pass