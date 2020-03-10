import mainwindow

from PyQt5 import QtWidgets, uic, QtCore

loginWindow = uic.loadUiType("login.ui")[0]


class FirstWindow(QtWidgets.QDialog, loginWindow):
    signedin = False

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.incorrectDetails.hide()

    def accept(self):
        self.signedin = True
        self.close()


'''def main():
    close = False
    # Handle high resolution displays:
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    login = FirstWindow(None)
    login.show()
    app.exec_()


if __name__ == '__main__':
    main()'''

