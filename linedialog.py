from PyQt5.QtCore import QDate

import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit, QComboBox


linesAddDialog = uic.loadUiType("LinesAdd.ui")[0]
db = 'Book Selling Database.db'


class LineDialog(QtWidgets.QDialog, linesAddDialog):
    def __init__(self, number, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.orderNumber = number

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

        linePrice = stockPrice*quantity

        data = (self.orderNumber, stockCode, quantity, linePrice)

        # find database
        datalayer.AddLineDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()
