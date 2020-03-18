from PyQt5.QtCore import QDate

import datalayer
import validator

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox

headerAddDialog = uic.loadUiType("HeaderAdd.ui")[0]
db = 'Book Selling Database.db'


class HeaderDialog(QtWidgets.QDialog, headerAddDialog):
    customerID = None

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.errorLabel.hide()

        results = datalayer.customer_name(db, True)
        comboBox: QComboBox = self.customerNameComboBox
        for row in results:
            # Add the customer name
            name: str = [str(x) for x in row][0]
            comboBox.addItem(name)

        # set the order date to today's date
        self.orderDateEdit.setDate(QDate.currentDate())

    def find_data(self):
        # convert text boxes to variables

        customerName = self.customerNameComboBox.currentText()
        self.customerID = datalayer.find_customer_id(db, customerName)
        deliveryAddress = self.deliveryAddressLineEdit.text()
        deliveryCharge = self.deliveryChargeLineEdit.text()

        if validator.invalid_number(deliveryCharge):
            self.errorLabel.setText("The delivery charge must be numeric")
            self.errorLabel.show()
            return False

        if validator.invalid_text(deliveryAddress):
            if not datalayer.find_address(db, self.customerID):
                self.errorLabel.setText("You must enter a delivery address if the customer does not have a default "
                                        "address")
                self.errorLabel.show()
                return False
            else:
                deliveryAddress = datalayer.find_address(db, self.customerID)

        # change orderDate into date format
        orderDate = self.orderDateEdit.date().toPyDate()
        orderCost = deliveryCharge

        data = (self.customerID, deliveryAddress, deliveryCharge, orderDate, orderCost)

        # find database
        datalayer.add_header_details(db, data)

        return True

    def accept(self):
        close = self.find_data()
        if close:
            self.close()
