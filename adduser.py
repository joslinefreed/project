
import datalayer

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox

import validator

userAddDialog = uic.loadUiType("UserAdd.ui")[0]
db = 'Book Selling Database.db'


class UserDialog(QtWidgets.QDialog, userAddDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.errorLabel.hide()

    def find_data(self):
        userName = self.nameLineEdit.text()
        password = self.passwordLineEdit.text()

        if validator.invalid_text(userName):
            self.errorLabel.setText("Please enter a user name")
            self.errorLabel.show()
            return False

        if validator.invalid_password(password):
            self.errorLabel.setText("Password must be at least 8 characters")
            self.errorLabel.show()
            return False

        administrator = self.administratorCheckBox.checkState()

        hashedPassword = validator.hash_password(password)
        data = (userName, hashedPassword, administrator)

        datalayer.add_user(db, data)

        return True

    def accept(self):
        close = self.find_data()
        if close:
            self.close()
