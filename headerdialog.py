from PyQt5.QtCore import QDate

import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox

headerAddDialog = uic.loadUiType("HeaderAdd.ui")[0]
db = 'Book Selling Database.db'


class HeaderDialog(QtWidgets.QDialog, headerAddDialog):

    customerID = None

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

        def setnumber(text):
            if text != '':
                return text
            else:
                return 0

        def setaddress(text):
            if text != '':
                return text
            else:
                text = datalayer.findAddress(db, self.customerID)
                return text

        customerName = self.customerNameComboBox.currentText()
        self.customerID = datalayer.findCustomerID(db, customerName)

        deliveryAddress = setaddress(self.deliveryAddressLineEdit.text())
        deliveryCharge = setnumber(self.deliveryChargeLineEdit.text())
        # change orderDate into date format
        orderDate = self.orderDateEdit.date().toPyDate()
        print(orderDate)
        orderCost = deliveryCharge
        data = (self.customerID, deliveryAddress, deliveryCharge, orderDate, orderCost)

        # find database
        datalayer.AddHeaderDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()
