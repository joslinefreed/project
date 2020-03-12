import datalayer

from PyQt5 import QtWidgets, uic, QtCore

loginWindow = uic.loadUiType("login.ui")[0]
db = 'Book Selling Database.db'


class FirstWindow(QtWidgets.QDialog, loginWindow):
    signedin = False

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.incorrectDetails.hide()
        self.username = None
        self.password = None

    def accept(self):

        self.getData()
        validPassword = datalayer.checkLogin(db, self.username)

        if self.password == validPassword:
            self.signedin = True
            self.close()
        else:
            self.nameLineEdit.clear()
            self.passwordLineEdit.clear()
            self.incorrectDetails.show()

    def getData(self):
        self.username = self.nameLineEdit.text()
        self.password = self.passwordLineEdit.text()
