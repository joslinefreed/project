import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit, QComboBox

import validator

customerUpdateDialog = uic.loadUiType("CustomerUpdate.ui")[0]
db = 'Book Selling Database.db'


class CustomerUpdate(QtWidgets.QDialog, customerUpdateDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        results = datalayer.customer_name(db, True)
        comboBox: QComboBox = self.nameComboBox
        for row in results:
            # Add the customer name
            name: str = [str(x) for x in row][0]
            comboBox.addItem(name)

        self.customerID = None

    def refresh_line_edits(self, name):

        self.customerID = datalayer.find_customer_id(db, name)

        email = datalayer.find_customer_email(db, self.customerID)
        self.emailLineEdit.setText(email)
        tel = datalayer.find_customer_tel(db, self.customerID)
        self.telLineEdit.setText(tel)
        address = datalayer.find_customer_address(db, self.customerID)
        self.addressLineEdit.setText(address)
        discount = str(datalayer.find_customer_discount(db, self.customerID))
        self.discountLineEdit.setText(discount)

    def find_data(self):

        def set_variables(text):
            if text != '':
                return text
            else:
                return None

        email = set_variables(self.emailLineEdit.text())
        tel = set_variables(self.telLineEdit.text())
        address = set_variables(self.addressLineEdit.text())
        discount = self.discountLineEdit.text()

        if validator.invalid_number(discount):
            discount = 0

        datalayer.update_email(db, email, self.customerID)
        datalayer.update_tel(db, tel, self.customerID)
        datalayer.update_address(db, address, self.customerID)
        datalayer.update_discount(db, discount, self.customerID)

    def accept(self):
        self.find_data()
        self.close()
