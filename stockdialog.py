import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit
stockAddDialog = uic.loadUiType("StockAdd.ui")[0]
db = 'Book Selling Database.db'


class StockDialog(QtWidgets.QDialog, stockAddDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def findData(self) -> QPlainTextEdit:

        # if blank enter None
        def setvaribles(text):
            if text != '':
                return text
            else:
                return None

        def setnumbers(text):
            if text != '':
                return text
            else:
                return 0

        # convert text boxes to variables
        title = self.titleLineEdit.text()
        author = setvaribles(self.authorLineEdit.text())
        listPrice = setnumbers(self.listPriceLineEdit.text())
        quantity = setnumbers(self.quantityLineEdit.text())
        data = (title, author, listPrice, quantity)

        # find database
        datalayer.AddStockDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()
