# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_registration_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegistrationWindow(object):
    def setupUi(self, RegistrationWindow):
        RegistrationWindow.setObjectName("RegistrationWindow")
        RegistrationWindow.resize(292, 214)
        self.layoutWidget = QtWidgets.QWidget(RegistrationWindow)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 271, 171))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.line_edit_username = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_edit_username.setText("")
        self.line_edit_username.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.line_edit_username.setObjectName("line_edit_username")
        self.verticalLayout.addWidget(self.line_edit_username)
        self.line_edit_password = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_edit_password.setObjectName("line_edit_password")
        self.verticalLayout.addWidget(self.line_edit_password)
        self.line_edit_password_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_edit_password_2.setObjectName("line_edit_password_2")
        self.verticalLayout.addWidget(self.line_edit_password_2)
        self.line_edit_birthday = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_edit_birthday.setObjectName("line_edit_birthday")
        self.verticalLayout.addWidget(self.line_edit_birthday)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_registration = QtWidgets.QPushButton(self.layoutWidget)
        self.button_registration.setObjectName("button_registration")
        self.horizontalLayout.addWidget(self.button_registration)
        self.button_cancel = QtWidgets.QPushButton(self.layoutWidget)
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout.addWidget(self.button_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RegistrationWindow)
        QtCore.QMetaObject.connectSlotsByName(RegistrationWindow)

    def retranslateUi(self, RegistrationWindow):
        _translate = QtCore.QCoreApplication.translate
        RegistrationWindow.setWindowTitle(_translate("RegistrationWindow", "Form"))
        self.line_edit_username.setPlaceholderText(_translate("RegistrationWindow", "?????? ????????????????????????"))
        self.line_edit_password.setPlaceholderText(_translate("RegistrationWindow", "????????????"))
        self.line_edit_password_2.setPlaceholderText(_translate("RegistrationWindow", "?????????????????? ????????????"))
        self.line_edit_birthday.setPlaceholderText(_translate("RegistrationWindow", "???????? ???????????????? (????????-????-????)"))
        self.button_registration.setText(_translate("RegistrationWindow", "??????????????????????"))
        self.button_cancel.setText(_translate("RegistrationWindow", "????????????"))
