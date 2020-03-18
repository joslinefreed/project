import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit, QComboBox

import validator

stockUpdateDialog = uic.loadUiType("StockUpdate.ui")[0]
db = 'Book Selling Database.db'


class StockUpdate(QtWidgets.QDialog, stockUpdateDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.errorLabel.hide()

        results = datalayer.stock_title(db, True)
        comboBox: QComboBox = self.titleComboBox
        for row in results:
            # Add the customer name
            name: str = [str(x) for x in row][0]
            comboBox.addItem(name)

        self.stockCode = None

    def refresh_line_edits(self, title):

        self.stockCode = datalayer.find_stock_code(db, title)

        price = str("{0:.2f}".format(datalayer.find_stock_price(db, self.stockCode)))
        self.listPriceLineEdit.setText(price)
        author = datalayer.find_author(db, self.stockCode)
        self.authorLineEdit.setText(author)
        quantity = str(datalayer.find_stock_quantity(db, self.stockCode))
        self.quantityLineEdit.setText(quantity)

    def find_data(self) -> bool:

        listPrice = self.listPriceLineEdit.text()
        author = self.authorLineEdit.text()
        quantity = self.quantityLineEdit.text()

        if validator.invalid_number(listPrice):
            self.errorLabel.setText("Price must be numeric")
            self.errorLabel.show()
            return False

        if validator.invalid_text(author):
            self.errorLabel.setText("Please enter an author")
            self.errorLabel.show()
            return False

        if validator.invalid_integer(self.quantityLineEdit.text()):
            self.errorLabel.setText("Quantity must be an integer")
            self.errorLabel.show()
            return False

        datalayer.update_author(db, author, self.stockCode)
        datalayer.update_stock_price(db, listPrice, self.stockCode)
        datalayer.update_quantity(db, quantity, self.stockCode)

        return True

    def accept(self):
        close = self.find_data()
        if close:
            self.close()
