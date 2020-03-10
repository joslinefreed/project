
import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox


linesAddDialog = uic.loadUiType("LinesAdd.ui")[0]
db = 'Book Selling Database.db'


class LineDialog(QtWidgets.QDialog, linesAddDialog):
    def __init__(self, number, name, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.orderNumber = number
        self.customerName = name

        lineResults = datalayer.StockTitle(db, True)
        comboBox: QComboBox = self.bookTitleComboBox
        for row in lineResults:
            # Add the customer name
            name: str = [str(x) for x in row][0]
            comboBox.addItem(name)

    def findData(self):

        # convert text boxes to variables
        bookTitle = self.bookTitleComboBox.currentText()
        stockCode = datalayer.findStockCode(db, bookTitle)

        quantity = int(self.quantityTextEdit.toPlainText())

        stockPrice = datalayer.findStockPrice(db, stockCode)

        discount = datalayer.findDiscount(db, self.customerName)

        if discount is None:
            discount = 1
        else:
            discount = 1-(discount/100)

        print("got here")
        linePrice = float("{0:.2f}".format(stockPrice*quantity*discount))

        data = (self.orderNumber, stockCode, quantity, linePrice)

        # find database
        datalayer.AddLineDetails(db, data)
        datalayer.UpdateOrderCost(db, self.orderNumber)
        pass

    def accept(self):
        self.findData()
        self.close()
