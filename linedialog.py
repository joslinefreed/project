
import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox

import validator

linesAddDialog = uic.loadUiType("LinesAdd.ui")[0]
db = 'Book Selling Database.db'


class LineDialog(QtWidgets.QDialog, linesAddDialog):
    def __init__(self, number, name, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.errorLabel.hide()
        self.orderNumber = int(number)
        self.customerName = name

        lineResults = datalayer.stock_title(db, True)
        comboBox: QComboBox = self.bookTitleComboBox
        for row in lineResults:
            # Add the customer name
            name: str = [str(x) for x in row][0]
            comboBox.addItem(name)

    def find_data(self):

        # convert text boxes to variables
        bookTitle = self.bookTitleComboBox.currentText()
        stockCode = datalayer.find_stock_code(db, bookTitle)
        quantity = self.quantityLineEdit.text()
        stockPrice = datalayer.find_stock_price(db, stockCode)
        discount = datalayer.find_discount(db, self.customerName)

        if validator.invalid_integer(quantity):
            self.errorLabel.setText("Quantity must be an integer")
            self.errorLabel.show()
            return False

        currentStock = datalayer.find_stock_quantity(db, stockCode)

        if (currentStock - int(quantity)) < 0:
            self.errorLabel.setText("There is not enough stock for this order")
            self.errorLabel.show()
            return False

        if validator.invalid_number(stockPrice):
            self.errorLabel.setText("Price must be numeric")
            self.errorLabel.show()
            return False

        if validator.invalid_number(discount):
            self.errorLabel.setText("Discount must be numeric")
            self.errorLabel.show()
            return False

        quantity = int(quantity)

        if discount is None:
            discount = 1
        else:
            discount = 1-(discount/100)

        linePrice = float("{0:.2f}".format(stockPrice*quantity*discount))

        data = (self.orderNumber, stockCode, quantity, linePrice)

        # find database
        datalayer.add_line_details(db, data)
        datalayer.update_order_cost(db, self.orderNumber)
        datalayer.reduce_quantity(db, str(quantity), stockCode)
        return True

    def accept(self):
        close = self.find_data()
        if close:
            self.close()
