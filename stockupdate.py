import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit, QComboBox

stockUpdateDialog = uic.loadUiType("StockUpdate.ui")[0]
db = 'Book Selling Database.db'


class StockUpdate(QtWidgets.QDialog, stockUpdateDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        results = datalayer.StockTitle(db, True)
        comboBox: QComboBox = self.titleComboBox
        for row in results:
            # Add the customer name
            name: str = [str(x) for x in row][0]
            comboBox.addItem(name)

        self.stockCode = None

    def refreshLineEdits(self, title):

        self.stockCode = datalayer.findStockCode(db, title)

        price = str("{0:.2f}".format(datalayer.findStockPrice(db, self.stockCode)))
        self.listPriceLineEdit.setText(price)
        author = datalayer.findAuthor(db, self.stockCode)
        self.authorLineEdit.setText(author)
        quantity = str(datalayer.findStockQuantity(db, self.stockCode))
        self.quantityLineEdit.setText(quantity)

    def findData(self) -> QPlainTextEdit:

        author = self.authorLineEdit.text()
        # datalayer.UpdateAuthor(db, author, self.stockCode)
        listPrice = self.listPriceLineEdit.text()
        datalayer.UpdateStockPrice(db, listPrice, self.stockCode)
        quantity = self.quantityLineEdit.text()
        datalayer.UpdateQuantity(db, quantity, self.stockCode)

        # find database
        #datalayer.UpdateStockDetails(db, listPrice, quantity, self.stockCode)
        pass

    def accept(self):
        self.findData()
        self.close()