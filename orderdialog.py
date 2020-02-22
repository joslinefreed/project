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
dialog2 = uic.loadUiType("LinesAdd.ui")[0]


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
        customerID = datalayer.findCustomerID(db, customerName)

        deliveryAddress = self.deliveryAddressTextEdit.toPlainText()
        deliveryCharge = setvaribles(self.deliveryChargeTextEdit.toPlainText())
        # change orderDate into date format
        orderDate = self.orderDateEdit.date().toPyDate()
        data = (customerID, deliveryAddress, deliveryCharge, orderDate)

        # find database
        datalayer.AddHeaderDetails(db, data)
        pass


class LineDialog(QtWidgets.QDialog, dialog2):
    def __init__(self, number, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.orderNumber = number

        results = datalayer.StockTitle(db)
        comboBox: QComboBox = self.bookTitleComboBox
        for row in results:
            # Add the customer name
            name: str = [str(x) for x in row][0]
            comboBox.addItem(name)

    def findData(self) -> QPlainTextEdit:
        # convert text boxes to variables

        def setvaribles(text):
            if text != '':
                return text
            else:
                pass

        bookTitle = self.bookTitleComboBox.currentText()
        stockCode = datalayer.findStockCode(db, bookTitle)

        quantity = self.quantityTextEdit.toPlainText()

        data = (self.orderNumber, stockCode, quantity)
        print(data)
        # find database
        datalayer.AddLineDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()
