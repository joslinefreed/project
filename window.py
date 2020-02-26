import sys

import datalayer
import stockdialog
import customerdialog
import headerdialog
import linedialog

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView

win1 = uic.loadUiType("Interface.ui")[0]
db = 'Book Selling Database.db'


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, number):

        # For numbers store float so can be compared numerically for sorting algorithms
        QTableWidgetItem.__init__(self, number, QTableWidgetItem.UserType)

        # Convert None to the value 0 to group all None as smallest value
        if number == "None":
            number = "0"
        self.__number = float(number)

    def __lt__(self, other):
        return self.__number < other.__number


class FirstWindow(QtWidgets.QMainWindow, win1):

    # Set all initial selected values to None
    selectedStockHeader = None
    selectedCustomerHeader = None
    selectedHeaderHeader = None
    selectedOrderNumber = None

    # define database so it can be used throughout the class
    db = 'Book Selling Database.db'

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        # load all the data into the tables
        self.setupUi(self)
        self.refreshStock()

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

    def refreshTab(self, tabnumber: int):
        if tabnumber == 0:
            self.refreshStock()
        elif tabnumber == 1:
            self.refreshCustomers()
        elif tabnumber == 2:
            self.refreshHeader()
        else:
            pass

    def refreshColumn(self, results, column, table, size, numeric=False):

        # Set the table to column to the size passed into the function
        table.setColumnWidth(column, size)

        # Set the row to the length of results
        row_count: int = len(results)
        table.setRowCount(row_count)

        # Set the starting index to 0
        row_index: int = 0

        for row in results:
            # Set the item in the table to being the name
            name: str = [str(x) for x in row][0]

            if numeric:
                # use our own class so that sorting of numeric values works correctly
                table.setItem(row_index, column, NumericTableWidgetItem(name))
            else:
                table.setItem(row_index, column, QTableWidgetItem(name))

            # Increment the row pointer
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

        # Read the data from the database and enter it into the relevant column
        title = datalayer.StockTitle(db)
        self.refreshColumn(title, 0, table, 150)
        author = datalayer.StockAuthor(db)
        self.refreshColumn(author, 1, table, 150)
        # Set numeric to True for price and quantity
        price = datalayer.StockListPrice(db)
        self.refreshColumn(price, 2, table, 50, True)
        quantity = datalayer.StockQuantity(db)
        self.refreshColumn(quantity, 3, table, 50, True)

    def addStock(self):

        # Open add stock dialog and then refresh stock
        stock_dialog = stockdialog.StockDialog()
        stock_dialog.exec_()
        self.refreshStock()

    def stockHeaderSectionClicked(self, logicalindex: int):
        # Find the stock table widget and header row
        table: QTableWidget = self.findStockTable()
        header: QHeaderView = table.horizontalHeader()

        # Check if the table is currently sorted in ascending order and if so sort in descending order
        if self.selectedStockHeader != logicalindex:
            table.sortItems(logicalindex, QtCore.Qt.AscendingOrder)
            # Change indicator on the header
            header.setSortIndicator(logicalindex, QtCore.Qt.AscendingOrder)
            # set selectedStockHeader to the new selected header index
            self.selectedStockHeader = logicalindex
        else:
            table.sortItems(logicalindex, QtCore.Qt.DescendingOrder)
            # Change indicator on the header
            header.setSortIndicator(logicalindex, QtCore.Qt.DescendingOrder)
            # reset selectedStockHeader as the column is currently sorted in descending order
            self.selectedStockHeader = None

        # Show the indicator
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

        # Read the data from the database and enter it into the relevant column
        names = datalayer.CustomerName(db)
        self.refreshColumn(names, 0, table, 100)
        email = datalayer.CustomerEmail(db)
        self.refreshColumn(email, 1, table, 100)
        tel = datalayer.CustomerTel(db)
        self.refreshColumn(tel, 2, table, 100)
        address = datalayer.CustomerAddress(db)
        self.refreshColumn(address, 3, table, 100)
        # Set numeric to true for discount
        discount = datalayer.CustomerDiscount(db)
        self.refreshColumn(discount, 4, table, 50, True)
        totalSpent = datalayer.CustomerTotalSpent(db)
        self.refreshColumn(totalSpent, 5, table, 50, True)

    def addCustomer(self):

        # Open add customer dialog and then refresh customer
        customer_dialog = customerdialog.CustomerDialog()
        customer_dialog.exec_()
        self.refreshCustomers()

    def customerHeaderSectionClicked(self, logicalindex: int):
        # Find the customer table widget and header row
        table: QTableWidget = self.findCustomerTable()
        header: QHeaderView = table.horizontalHeader()

        # Check if the table is currently sorted in ascending order and if so sort in descending order
        if self.selectedCustomerHeader != logicalindex:
            table.sortItems(logicalindex, QtCore.Qt.AscendingOrder)
            # Change indicator on the header
            header.setSortIndicator(logicalindex, QtCore.Qt.AscendingOrder)
            # Set selectedCustomerHeader to the new selected header index
            self.selectedCustomerHeader = logicalindex
        else:
            table.sortItems(logicalindex, QtCore.Qt.DescendingOrder)
            # Change an indicator on the header
            header.setSortIndicator(logicalindex, QtCore.Qt.DescendingOrder)
            # Reset selectedStockHeader as the column is currently sorted in descending order
            self.selectedCustomerHeader = None

        # Show the indicator
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

        # Read the data from the database and enter it into the relevant column
        customerName = datalayer.OrderCustomerName(db)
        self.refreshColumn(customerName, 0, table, 100)
        deliveryAddress = datalayer.OrderDeliveryAddress(db)
        self.refreshColumn(deliveryAddress, 1, table, 100)
        # Set numeric True for delivery charge
        deliveryCharge = datalayer.OrderDeliveryCharge(db)
        self.refreshColumn(deliveryCharge, 2, table, 75, True)
        date = datalayer.OrderDate(db)
        self.refreshColumn(date, 3, table, 75)
        totalCost = datalayer.OrderCost(db)
        self.refreshColumn(totalCost, 4, table, 45)
        # Set orderNumber column size to zero so it cant be seen
        orderNumber = datalayer.OrderNumber(db)
        self.refreshColumn(orderNumber, 5, table, 0)

    def addHeader(self):

        # Open add header dialog and then refresh header
        header_dialog = headerdialog.HeaderDialog()
        header_dialog.exec_()
        self.refreshHeader()

    def headerHorizontalHeaderSectionClicked(self, logicalindex: int):
        # Find the stock table widget and header row
        table: QTableWidget = self.findHeadersTable()
        header: QHeaderView = table.horizontalHeader()

        # Check if the table is currently sorted in ascending order and if so sort in descending order
        if self.selectedHeaderHeader != logicalindex:
            table.sortItems(logicalindex, QtCore.Qt.AscendingOrder)
            # Change indicator on the header
            header.setSortIndicator(logicalindex, QtCore.Qt.AscendingOrder)
            # Set selectedCustomerHeader to the new selected header index
            self.selectedHeaderHeader = logicalindex
        else:
            table.sortItems(logicalindex, QtCore.Qt.DescendingOrder)
            # Change indicator on the header
            header.setSortIndicator(logicalindex, QtCore.Qt.DescendingOrder)
            # Reset selectedHeaderHeader as the column is currently sorted in descending order
            self.selectedHeaderHeader = None
        header.setSortIndicatorShown(True)

    def headerVerticalHeaderSectionClicked(self, logicalindex: int):
        headersTable: QTableWidget = self.findHeadersTable()

        # find Order Number that has been selected
        self.selectedOrderNumber = headersTable.item(logicalindex, 5).text()

        # refresh the OrderLines for relevant order number
        self.refreshOrderLines()

        pass

    def refreshOrderLines(self):
        linesTable: QTableWidget = self.findLinesTable()

        # repeat the function for each column
        bookName = datalayer.OrderBookName(db, self.selectedOrderNumber)
        self.refreshColumn(bookName, 0, linesTable, 200)

        # Set numeric as true so it can be sorted correctly
        quantity = datalayer.OrderQuantity(db, self.selectedOrderNumber)
        self.refreshColumn(quantity, 1, linesTable, 100, True)
        lineCost = datalayer.OrderLineCost(db, self.selectedOrderNumber)
        self.refreshColumn(lineCost, 2, linesTable, 150, True)

    def findLinesTable(self) -> QTableWidget:
        # Find the order headers table widget
        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
        first_tab: QWidget = tab.findChild(QWidget, "ordersTab")
        table: QTableWidget = first_tab.findChild(QTableWidget, "linesTable")
        return table

    def addLines(self):
        if self.selectedOrderNumber is not None:
            line_dialog = linedialog.LineDialog(self.selectedOrderNumber)
            line_dialog.exec_()
            self.refreshOrderLines()
        else:
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
