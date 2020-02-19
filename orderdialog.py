import sys

from PyQt5.QtGui import QFocusEvent
from PyQt5.uic.properties import QtGui

import datalayer
import window

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QDialog, QPushButton, QPlainTextEdit, \
    QDialogButtonBox, QComboBox

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

    def findData(self) -> QPlainTextEdit:

        customerName = self.customerNameComboBox.currentText()
        # db = 'Book Selling Database.db'
        customerID = datalayer.findCustomerID(db, customerName)
        print(customerID)

        # convert text boxes to variables

        '''def setvaribles(text):
            if text != '':
                return text
            else:
                return None
                
        deliveryAddress = setvaribles(self.deliveryAddressTextEdit.toPlainText())
        deliveryCharge = setvaribles(self.deliveryChargeTextEdit.toPlainText())
        # might need to make it date a string
        orderDate = self.orderDateEdit.date().toPyDate()
        print(orderDate)
        data = (customerName, deliveryAddress, deliveryCharge, orderDate)
        print(data)'''
        # find database
        # datalayer.AddStockDetails(db, data)

    def accept(self):
        self.findData()
        self.close()