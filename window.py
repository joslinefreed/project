import sys

import datalayer
import customerdialog
import stockdialog

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QTableView, QDialog, \
    QPushButton, QPlainTextEdit, \
    QDialogButtonBox, QTextBrowser

win1 = uic.loadUiType("Interface.ui")[0]


class FirstWindow(QtWidgets.QMainWindow, win1):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # load all the data into the tables
        self.setupUi(self)
        self.refreshCustomers()
        self.refreshStock()
        self.refreshOrders()

        # hide help text

        self.helpWidget.hide()

        # Get the header view from the customer table and connect it for when the section is clicked
        customer_table: QTableWidget = self.findCustomerTable()
        customer_header: QHeaderView = customer_table.horizontalHeader()
        customer_header.sectionClicked.connect(self.customerHeaderSectionClicked)

        # Get the header view from the stock table and connect it for when the section is clicked
        stock_table: QTableWidget = self.findStockTable()
        stock_header: QHeaderView = stock_table.horizontalHeader()
        stock_header.sectionClicked.connect(self.stockHeaderSectionClicked)

    def customerHeaderSectionClicked(self, logical_index: int):
        # Find the customer table widget and sort the column
        table: QTableWidget = self.findCustomerTable()
        table.sortItems(logical_index, QtCore.Qt.AscendingOrder)
        header: QHeaderView = table.horizontalHeader()

    def stockHeaderSectionClicked(self, logical_index: int):
        # Find the stock table widget and sort the column
        table: QTableWidget = self.findStockTable()
        table.sortItems(logical_index, QtCore.Qt.AscendingOrder)

    def myRead(self):
        db = 'Book Selling Database.db'
        print()
        print("Reading customer details from the database:")
        results = datalayer.CustomerDetails(db)
        for row in results:
            print('\t'.join([str(x) for x in row]))

        print()
        print("Reading order customer names from the database:")
        results = datalayer.OrderCustomerName(db)
        for row in results:
                print('\t'.join([str(x) for x in row]))

    def refreshColumn(self, results, column, table):

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
                # Set the item in the table to being the name
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


    #def findCurrentTable(self) -> QTableWidget:
    #    # Find the current table widget that is shown
    #    tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
    #    index = tab.currentIndex()
    #    print(index)
    #    table: QTableWidget = None
    #    if index == 1:
    #        first_tab: QWidget = tab.findChild(QWidget, "customerTab")
    #        table = first_tab.findChild(QTableWidget, "customerTable")
    #    elif index == 2:
    #        first_tab: QWidget = tab.findChild(QWidget, "stockTab")
    #        table = first_tab.findChild(QTableWidget, "stockTable")
    #    return table

    def refreshCustomers(self):
        db = 'Book Selling Database.db'

        # Find the customer table widget
        table: QTableWidget = self.findCustomerTable()

        # iterate each row for a specific column

        # repeat the function for each column
        names = datalayer.CustomerName(db)
        self.refreshColumn(names, 0, table)

        email = datalayer.CustomerEmail(db)
        self.refreshColumn(email, 1, table)

        tel = datalayer.CustomerTel(db)
        self.refreshColumn(tel, 2, table)

        address = datalayer.CustomerAddress(db)
        self.refreshColumn(address, 3, table)

        discount = datalayer.CustomerDiscount(db)
        self.refreshColumn(discount, 4, table)

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
        self.refreshColumn(title, 0, table)

        author = datalayer.StockAuthor(db)
        self.refreshColumn(author, 1, table)

        price = datalayer.StockListPrice(db)
        self.refreshColumn(price, 2, table)

        quantity = datalayer.StockQuantity(db)
        self.refreshColumn(quantity, 3, table)

    def addStock(self):
        stock_dialog = stockdialog.StockDialog()
        stock_dialog.exec_()

    def findOrdersTable(self) -> QTableWidget:
        # Find the order headers table widget
        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        first_tab: QWidget = tab.findChild(QWidget, "ordersTab")
        table: QTableWidget = first_tab.findChild(QTableWidget, "headersTable")
        return table

    def refreshOrders(self):

        db = 'Book Selling Database.db'

        # Find the stock table widget
        table: QTableWidget = self.findOrdersTable()

        # repeat the function for each column
        customerName = datalayer.OrderCustomerName(db)
        self.refreshColumn(customerName, 0, table)

        deliveryAddress = datalayer.OrderDeliveryAddress(db)
        self.refreshColumn(deliveryAddress, 1, table)

        deliveryCharge = datalayer.OrderDeliveryCharge(db)
        self.refreshColumn(deliveryCharge, 2, table)

        date = datalayer.OrderDate(db)
        self.refreshColumn(date, 3, table)

    def help(self):
        self.helpWidget.show()

    def closeHelp(self):
        self.helpWidget.hide()


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
