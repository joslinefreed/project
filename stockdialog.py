import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit

import validator

stockAddDialog = uic.loadUiType("StockAdd.ui")[0]
db = 'Book Selling Database.db'


class StockDialog(QtWidgets.QDialog, stockAddDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.errorLabel.hide()

    def find_data(self) -> bool:

        # convert text boxes to variables

        if validator.invalid_text(self.titleLineEdit.text()):
            self.errorLabel.setText("Please enter a book title")
            self.errorLabel.show()
            return False

        if validator.invalid_number(self.listPriceLineEdit.text()):
            self.errorLabel.setText("Price must be numeric")
            self.errorLabel.show()
            return False

        if validator.invalid_text(self.authorLineEdit.text()):
            self.errorLabel.setText("Please enter an author")
            self.errorLabel.show()
            return False

        if validator.invalid_integer(self.quantityLineEdit.text()):
            self.errorLabel.setText("Quantity must be an integer")
            self.errorLabel.show()
            return False

        title = self.titleLineEdit.text()
        author = self.authorLineEdit.text()
        listPrice = self.listPriceLineEdit.text()
        quantity = self.quantityLineEdit.text()

        data = (title, author, listPrice, quantity)
        datalayer.add_stock_details(db, data)

        return True

    def accept(self):

        close = self.find_data()
        if close:
            self.close()
