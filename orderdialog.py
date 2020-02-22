import sys

from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtGui import QFocusEvent
from PyQt5.uic.properties import QtGui

import datalayer
import window

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QDialog, QPushButton, QPlainTextEdit, \
    QDialogButtonBox, QComboBox, QDateEdit, QDateTimeEdit

db = 'Book Selling Database.db'
dialog1 = uic.loadUiType("HeaderAdd.ui")[0]


class HeaderDialog(QtWidgets.QDialog, dialog1):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        results = datalayer.CustomerName(db, True)
        comboBox: QComboBox = self.customerNameComboBox
        for row in results:
            # Add the customer name
            name: str = [str(x) for x in row][0]
            comboBox.addItem(name)

        # set the order date to today's date
        self.orderDateEdit.setDate(QDate.currentDate())

    def findData(self) -> QPlainTextEdit:
        # convert text boxes to variables

        def setvaribles(text):
            if text != '':
                return text
            else:
                return None

        customerName = self.customerNameComboBox.currentText()
        # db = 'Book Selling Database.db'
        customerID = datalayer.findCustomerID(db, customerName)
        print(customerID)

        deliveryAddress = setvaribles(self.deliveryAddressTextEdit.toPlainText())
        deliveryCharge = setvaribles(self.deliveryChargeTextEdit.toPlainText())
        # might need to make it date a string
        orderDate = self.orderDateEdit.date().toPyDate()
        data = (customerID, deliveryAddress, deliveryCharge, orderDate)
        print(data)
        # find database
        datalayer.AddHeaderDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()
