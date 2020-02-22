import sys

import datalayer
import customerdialog
import stockdialog
import orderdialog

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QTableView, QDialog, \
    QPushButton, QPlainTextEdit, \
    QDialogButtonBox, QTextBrowser

win1 = uic.loadUiType("Interface.ui")[0]


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, number):
        QTableWidgetItem.__init__(self, number, QTableWidgetItem.UserType)
        if number == "None":
            number = "-1"
        self.__number = float(number)

    def __lt__(self, other):
        return self.__number < other.__number


class FirstWindow(QtWidgets.QMainWindow, win1):

    selectedStockHeader = None
    selectedCustomerHeader = None
    selectedHeaderHeader = None

    db = 'Book Selling Database.db'

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # load all the data into the tables
        self.setupUi(self)
        self.refreshCustomers()
        self.refreshStock()
        self.refreshHeader()

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

        # Get the header view from the stock table and connect it for when the section is clicked
        headers_table: QTableWidget = self.findHeadersTable()
        headers_horizontal_header: QHeaderView = headers_table.horizontalHeader()
        headers_horizontal_header.sectionClicked.connect(self.headerHorizontalHeaderSectionClicked)
        headers_vertical_header: QHeaderView = headers_table.verticalHeader()
        headers_vertical_header.sectionClicked.connect(self.headerVerticalHeaderSectionClicked)

    def refreshColumn(self, results, column, table, size, numeric=False):

        table.setColumnWidth(column, size)
        row_count: int = len(results)
        table.setRowCount(row_count)
        row_index: int = 0

        for row in results:
            # Set the item in the table to being the name
            name: str = [str(x) for x in row][0]

            if numeric:
                # use our own class so that sorting of numeric values works correctly
                table.setItem(row_index, column, NumericTableWidgetItem(name))
            else:
                table.setItem(row_index, column, QTableWidgetItem(name))
            row_index = row_index + 1

    def findStockTable(self) -> QTableWidget:
        # Find the stock table widget
        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        first_tab: QWidget = tab.findChild(QWidget, "stockTab")
        table: QTableWidget = first_tab.findChild(QTableWidget, "stockTable")

        return table

    def refreshStock(self):

        # Find the stock table widget
        table: QTableWidget = self.findStockTable()

        # repeat the function for each column
        title = datalayer.StockTitle(self.db)
        self.refreshColumn(title, 0, table, 150)
        author = datalayer.StockAuthor(self.db)
        self.refreshColumn(author, 1, table, 150)
        price = datalayer.StockListPrice(self.db)
        self.refreshColumn(price, 2, table, 50, True)
        quantity = datalayer.StockQuantity(self.db)
        self.refreshColumn(quantity, 3, table, 50, True)

    def addStock(self):
        stock_dialog = stockdialog.StockDialog()
        stock_dialog.exec_()
        self.refreshStock()

    def stockHeaderSectionClicked(self, logicalindex: int):
        # Find the stock table widget and sort the column
        table: QTableWidget = self.findStockTable()
        header: QHeaderView = table.horizontalHeader()
        if self.selectedStockHeader != logicalindex:
            table.sortItems(logicalindex, QtCore.Qt.AscendingOrder)
            header.setSortIndicator(logicalindex, QtCore.Qt.AscendingOrder)
            self.selectedStockHeader = logicalindex
        else:
            table.sortItems(logicalindex, QtCore.Qt.DescendingOrder)
            header.setSortIndicator(logicalindex, QtCore.Qt.DescendingOrder)
            self.selectedStockHeader = None
        header.setSortIndicatorShown(True)

    def searchStock(self):
        pass

    def findCustomerTable(self) -> QTableWidget:
        # Find the customer table widget
        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        first_tab: QWidget = tab.findChild(QWidget, "customerTab")
        table: QTableWidget = first_tab.findChild(QTableWidget, "customerTable")

        return table

    def refreshCustomers(self):
        # Find the customer table widget
        table: QTableWidget = self.findCustomerTable()

        # iterate each row for a specific column

        # repeat the function for each column
        names = datalayer.CustomerName(self.db)
        self.refreshColumn(names, 0, table, 100)
        email = datalayer.CustomerEmail(self.db)
        self.refreshColumn(email, 1, table, 100)
        tel = datalayer.CustomerTel(self.db)
        self.refreshColumn(tel, 2, table, 100)
        address = datalayer.CustomerAddress(self.db)
        self.refreshColumn(address, 3, table, 100)
        discount = datalayer.CustomerDiscount(self.db)
        self.refreshColumn(discount, 4, table, 50, True)

    def addCustomer(self):
        customer_dialog = customerdialog.CustomerDialog()
        customer_dialog.exec_()
        self.refreshCustomers()

    def customerHeaderSectionClicked(self, logicalindex: int):
        # Find the customer table widget and sort the column
        table: QTableWidget = self.findCustomerTable()
        header: QHeaderView = table.horizontalHeader()
        if self.selectedCustomerHeader != logicalindex:
            table.sortItems(logicalindex, QtCore.Qt.AscendingOrder)
            header.setSortIndicator(logicalindex, QtCore.Qt.AscendingOrder)
            self.selectedCustomerHeader = logicalindex
        else:
            table.sortItems(logicalindex, QtCore.Qt.DescendingOrder)
            header.setSortIndicator(logicalindex, QtCore.Qt.DescendingOrder)
            self.selectedCustomerHeader = None
        header.setSortIndicatorShown(True)

    def searchCustomers(self):
        pass

    def findHeadersTable(self) -> QTableWidget:
        # Find the order headers table widget
        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        first_tab: QWidget = tab.findChild(QWidget, "ordersTab")
        table: QTableWidget = first_tab.findChild(QTableWidget, "headersTable")
        return table

    def refreshHeader(self):

        # Find the stock table widget
        table: QTableWidget = self.findHeadersTable()

        # repeat the function for each column
        customerName = datalayer.OrderCustomerName(self.db)
        self.refreshColumn(customerName, 0, table, 100)
        deliveryAddress = datalayer.OrderDeliveryAddress(self.db)
        self.refreshColumn(deliveryAddress, 1, table, 100)
        deliveryCharge = datalayer.OrderDeliveryCharge(self.db)
        self.refreshColumn(deliveryCharge, 2, table, 75, True)
        date = datalayer.OrderDate(self.db)
        self.refreshColumn(date, 3, table, 75)
        orderNumber = datalayer.OrderNumber(self.db)
        self.refreshColumn(orderNumber, 3, table, 0)

    def addHeader(self):
        order_dialog = orderdialog.HeaderDialog()
        order_dialog.exec_()
        self.refreshHeaders()

    def headerHorizontalHeaderSectionClicked(self, logicalindex: int):
        # Find the stock table widget and sort the column
        table: QTableWidget = self.findHeadersTable()
        header: QHeaderView = table.horizontalHeader()
        if self.selectedHeaderHeader != logicalindex:
            table.sortItems(logicalindex, QtCore.Qt.AscendingOrder)
            header.setSortIndicator(logicalindex, QtCore.Qt.AscendingOrder)
            self.selectedHeaderHeader = logicalindex
        else:
            table.sortItems(logicalindex, QtCore.Qt.DescendingOrder)
            header.setSortIndicator(logicalindex, QtCore.Qt.DescendingOrder)
            self.selectedHeaderHeader = None
        header.setSortIndicatorShown(True)

    def headerVerticalHeaderSectionClicked(self, logicalindex: int):
        linesTable: QTableWidget = self.findLinesTable()
        headersTable: QTableWidget = self.findHeadersTable()
        #find Order Number
        #orderNumber = datalayer.findOrderNumber(logicalindex)

        orderNumber = headersTable.item(logicalindex, 3).text()
        print(orderNumber)
        # repeat the function for each column
        bookName = datalayer.OrderBookName(self.db, orderNumber)
        self.refreshColumn(bookName, 0, linesTable, 200)

        quantity = datalayer.OrderQuantity(self.db, orderNumber)
        print(quantity)
        self.refreshColumn(quantity, 1, linesTable, 100, True)

        '''lineCost = datalayer.OrderLineCost(self.db)
        self.refreshColumn(lineCost, 2, table, 150)'''
        pass

    def findLinesTable(self) -> QTableWidget:
        # Find the order headers table widget
        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        first_tab: QWidget = tab.findChild(QWidget, "ordersTab")
        table: QTableWidget = first_tab.findChild(QTableWidget, "linesTable")
        return table

    def addLines(self):
        pass

    def searchOrders(self):
        pass

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
