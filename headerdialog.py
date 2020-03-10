from PyQt5.QtCore import QDate

import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox

headerAddDialog = uic.loadUiType("HeaderAdd.ui")[0]
db = 'Book Selling Database.db'


class HeaderDialog(QtWidgets.QDialog, headerAddDialog):
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

    def findData(self):
        # convert text boxes to variables

        def setvaribles(text):
            if text != '':
                return text
            else:
                return 0

        customerName = self.customerNameComboBox.currentText()
        customerID = datalayer.findCustomerID(db, customerName)

        deliveryAddress = self.deliveryAddressTextEdit.toPlainText()
        deliveryCharge = setvaribles(self.deliveryChargeTextEdit.toPlainText())
        # change orderDate into date format
        orderDate = self.orderDateEdit.date().toPyDate()
        orderCost = deliveryCharge
        data = (customerID, deliveryAddress, deliveryCharge, orderDate, orderCost)

        # find database
        datalayer.AddHeaderDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()
