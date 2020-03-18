import datalayer

from PyQt5 import QtWidgets, uic, QtCore

import validator

loginWindow = uic.loadUiType("login.ui")[0]
db = 'Book Selling Database.db'


class FirstWindow(QtWidgets.QDialog, loginWindow):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.incorrectDetails.hide()
        self.username = None
        self.password = None
        self.signedIn = False
        self.administrator = False

    def accept(self):

        self.get_data()

        password = validator.hash_password(self.password)
        validPassword = datalayer.check_login(db, self.username)

        if password == validPassword:
            self.signedIn = True
            administrator = datalayer.find_administrator(db, self.username)
            if administrator == 1:
                self.administrator = True
            self.close()
        else:
            self.nameLineEdit.clear()
            self.passwordLineEdit.clear()
            self.incorrectDetails.show()

    def get_data(self):
        self.username = self.nameLineEdit.text()
        self.password = self.passwordLineEdit.text()


'''def hash_password(password):
    crypt = hashlib.md5()
    crypt.update(bytearray(password, 'utf-8'))
    print(crypt.hexdigest())'''

