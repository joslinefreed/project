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

        def setnumber(text):
            if text != '':
                return text
            else:
                return 0

        # convert text boxes to variables
        name = self.nameLineEdit.text()
        email = setvaribles(self.emailLineEdit.text())
        tel = setvaribles(self.telLineEdit.text())
        address = setvaribles(self.addressLineEdit.text())
        discount = setnumber(self.discountLineEdit.text())
        totalspent = 0
        data = (name, email, tel, address, discount, totalspent)

        # add into database
        datalayer.AddCustomerDetails(db, data)
        pass

    def accept(self):
        self.findData()
        self.close()

