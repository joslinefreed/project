import sys

import datalayer
import customerdialog
import stockdialog

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QDialog, QPushButton, QPlainTextEdit, \
    QDialogButtonBox

win1 = uic.loadUiType("Interface.ui")[0]


class FirstWindow(QtWidgets.QMainWindow, win1):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.refreshCustomers()
        self.refreshStock()

    def myRead(self):
        print("Reading customer details the database:")

        db = 'Book Selling Database.db'
        results = datalayer.CustomerDetails(db)
        for row in results:
            print('\t'.join([str(x) for x in row]))

    def refresh_column(self, results, column, table):

        table.setColumnWidth(column, 100)
        row_count: int = len(results) - 1
        table.setRowCount(row_count)

        row_index: int = 0
        heading_row = True
        for row in results:
            if heading_row:
                # Skip the heading by not adding it
                heading_row = False
            else:
                # Set the item in the table to being the customer name
                name: str = [str(x) for x in row][0]
                item: QTableWidgetItem = QTableWidgetItem(name)
                table.setItem(row_index, column, QTableWidgetItem(name))
                row_index = row_index + 1

    def findCustomerTable(self) -> QTableWidget:
        # Find the customer table widget
        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        first_tab: QWidget = tab.findChild(QWidget, "customerTab")
        table: QTableWidget = first_tab.findChild(QTableWidget, "customerTable")

        return table

    def refreshCustomers(self):
        db = 'Book Selling Database.db'

        # Find the customer table widget
        table: QTableWidget = self.findCustomerTable()

        # iterate each row for a specific column

        # repeat the function for each column
        names = datalayer.CustomerName(db)
        self.refresh_column(names, 0, table)

        email = datalayer.CustomerEmail(db)
        self.refresh_column(email, 1, table)

        tel = datalayer.CustomerTel(db)
        self.refresh_column(tel, 2, table)

        address = datalayer.CustomerAddress(db)
        self.refresh_column(address, 3, table)

        discount = datalayer.CustomerDiscount(db)
        self.refresh_column(discount, 4, table)

    def addCustomer(self):
        customer_dialog = customerdialog.CustomerDialog()
        customer_dialog.exec_()

        '''
        # Find the customer table widget
        table: QTableWidget = self.findCustomerTable()

        # if there are no rows
        if table.rowCount() == 0:
            # Refresh the customers
            self.refreshCustomers()

        # add a row
        row_count = table.rowCount() + 1
        table.setRowCount(row_count)

        print("Add Customer")
        '''

    def findStockTable(self) -> QTableWidget:
        # Find the stock table widget
        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        first_tab: QWidget = tab.findChild(QWidget, "stockTab")
        table: QTableWidget = first_tab.findChild(QTableWidget, "stockTable")

        return table

    def refreshStock(self):

        db = 'Book Selling Database.db'

        # Find the stock table widget
        table: QTableWidget = self.findStockTable()

        # repeat the function for each column
        title = datalayer.StockTitle(db)
        self.refresh_column(title, 0, table)

        author = datalayer.StockAuthor(db)
        self.refresh_column(author, 1, table)

        price = datalayer.StockListPrice(db)
        self.refresh_column(price, 2, table)

        quantity = datalayer.StockQuantity(db)
        self.refresh_column(quantity, 3, table)

    def addStock(self):
        stock_dialog = stockdialog.StockDialog()
        stock_dialog.exec_()

    def refreshOrders(self):

        db = 'Book Selling Database.db'

        # Find the stock table widget
        table: QTableWidget = self.findStockTable()

        # repeat the function for each column
        title = datalayer.StockTitle(db)
        self.refresh_column(title, 0, table)

        author = datalayer.StockAuthor(db)
        self.refresh_column(author, 1, table)

        price = datalayer.StockListPrice(db)
        self.refresh_column(price, 2, table)

        quantity = datalayer.StockQuantity(db)
        self.refresh_column(quantity, 3, table)


def main():
    # Handle high resolution displays:
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    window1 = FirstWindow(None)
    window1.show()
    app.exec_()


if __name__ == '__main__':
    main()
