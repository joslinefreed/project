import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit

import validator

customerAddDialog = uic.loadUiType("CustomerAdd.ui")[0]
db = 'Book Selling Database.db'


class CustomerDialog(QtWidgets.QDialog, customerAddDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.errorLabel.hide()

    def find_data(self) -> bool:

        def set_variables(text):
            if text != '':
                return text
            else:
                return None

        name = self.nameLineEdit.text()
        email = set_variables(self.emailLineEdit.text())
        tel = set_variables(self.telLineEdit.text())
        address = set_variables(self.addressLineEdit.text())
        discount = self.discountLineEdit.text()

        if validator.invalid_text(name):
            self.errorLabel.setText("Please enter a customer name")
            self.errorLabel.show()
            return False

        if validator.invalid_number(self.listPriceLineEdit.text()):
            discount = 0

        # convert text boxes to variables5
        totalSpent = 0
        data = (name, email, tel, address, discount, totalSpent)

        # add into database
        datalayer.add_customer_details(db, data)

        return True

    def accept(self):
        close = self.find_data()
        if close:
            self.close()

