import sys

from PyQt5.QtGui import QFocusEvent
from PyQt5.uic.properties import QtGui

import datalayer
import window

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QDialog, QPushButton, QPlainTextEdit, \
    QDialogButtonBox

#copied from stock need to change

dialog1 = uic.loadUiType("StockAdd.ui")[0]


class StockDialog(QtWidgets.QDialog, dialog1):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

    def findData(self) -> QPlainTextEdit:

        # convert text boxes to variables

        def setvaribles(text):
            if text != '':
                return text
            else:
                return None

        title = setvaribles(self.titleTextEdit.toPlainText())
        author = setvaribles(self.authorTextEdit.toPlainText())
        listPrice = setvaribles(self.listPriceTextEdit.toPlainText())
        quantity = setvaribles(self.quantityTextEdit.toPlainText())
        data = (title, author, listPrice, quantity)
        print(data)
        # find database
        db = 'Book Selling Database.db'
        datalayer.AddStockDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()