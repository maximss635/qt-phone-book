# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(726, 525)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(160, 70, 471, 251))
        self.widget.setObjectName("widget")
        self.main_layout = QtWidgets.QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")
        self.label_hello = QtWidgets.QLabel(self.widget)
        self.label_hello.setObjectName("label_hello")
        self.main_layout.addWidget(self.label_hello)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.navigation_panel = QtWidgets.QListWidget(self.widget)
        self.navigation_panel.setObjectName("navigation_panel")
        item = QtWidgets.QListWidgetItem()
        self.navigation_panel.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.navigation_panel.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.navigation_panel.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.navigation_panel.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.navigation_panel.addItem(item)
        self.horizontalLayout_2.addWidget(self.navigation_panel)
        self.main_table = QtWidgets.QTableWidget(self.widget)
        self.main_table.setObjectName("main_table")
        self.main_table.setColumnCount(3)
        self.main_table.setRowCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.main_table.setHorizontalHeaderItem(2, item)
        self.horizontalLayout_2.addWidget(self.main_table)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_add = QtWidgets.QPushButton(self.widget)
        self.button_add.setObjectName("button_add")
        self.horizontalLayout.addWidget(self.button_add)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.main_layout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsfsdf = QtWidgets.QAction(MainWindow)
        self.actionsfsdf.setObjectName("actionsfsdf")
        self.actionsdfsdf = QtWidgets.QAction(MainWindow)
        self.actionsdfsdf.setObjectName("actionsdfsdf")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_hello.setText(_translate("MainWindow", "TextLabel"))
        __sortingEnabled = self.navigation_panel.isSortingEnabled()
        self.navigation_panel.setSortingEnabled(False)
        item = self.navigation_panel.item(0)
        item.setText(_translate("MainWindow", "аб"))
        item = self.navigation_panel.item(1)
        item.setText(_translate("MainWindow", "вг"))
        item = self.navigation_panel.item(2)
        item.setText(_translate("MainWindow", "де"))
        item = self.navigation_panel.item(3)
        item.setText(_translate("MainWindow", "жз"))
        item = self.navigation_panel.item(4)
        item.setText(_translate("MainWindow", "ий"))
        self.navigation_panel.setSortingEnabled(__sortingEnabled)
        item = self.main_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Новая строка"))
        item = self.main_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Новая строка"))
        item = self.main_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Новая строка"))
        item = self.main_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Новая строка"))
        item = self.main_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Имя"))
        item = self.main_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Телефон"))
        item = self.main_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Дата рождения"))
        self.button_add.setText(_translate("MainWindow", "Добавить"))
        self.actionsfsdf.setText(_translate("MainWindow", "sfsdf"))
        self.actionsdfsdf.setText(_translate("MainWindow", "sdfsdf"))
