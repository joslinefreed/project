import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit


customerAddDialog = uic.loadUiType("CustomerAdd.ui")[0]
db = 'Book Selling Database.db'


class CustomerDialog(QtWidgets.QDialog, customerAddDialog):
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

        # convert text boxes to variables
        name = self.nameTextEdit.toPlainText()
        email = setvaribles(self.emailTextEdit.toPlainText())
        tel = setvaribles(self.telTextEdit.toPlainText())
        address = setvaribles(self.addressTextEdit.toPlainText())
        discount = setvaribles(self.discountTextEdit.toPlainText())
        data = (name, email, tel, address, discount)
        # find database
        datalayer.AddCustomerDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()

