import sys

from PyQt5.QtGui import QFocusEvent
from PyQt5.uic.properties import QtGui

import datalayer

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QDialog, QPushButton, QPlainTextEdit, \
    QDialogButtonBox

import window

dialog1 = uic.loadUiType("CustomerAdd.ui")[0]


class CustomerDialog(QtWidgets.QDialog, dialog1):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def findData(self) -> QPlainTextEdit:

        # convert text boxes to variables

        def setvaribles(text):
            if text != '':
                return text
            else:
                return None

        name = setvaribles(self.nameTextEdit.toPlainText())
        email = setvaribles(self.emailTextEdit.toPlainText())
        tel = setvaribles(self.telTextEdit.toPlainText())
        address = setvaribles(self.addressTextEdit.toPlainText())
        discount = setvaribles(self.discountTextEdit.toPlainText())
        data = (name, email, tel, address, discount)
        # find database
        db = 'Book Selling Database.db'
        datalayer.AddCustomerDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()
