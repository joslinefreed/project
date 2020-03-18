import sys

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.uic.properties import QtGui

import adduser
import customerdialog
import datalayer
import headerdialog
import linedialog
import login
import stockdialog
import stockupdate
from customerupdate import CustomerUpdate

win1 = uic.loadUiType("Interface.ui")[0]
db = 'Book Selling Database.db'

sys._excepthook = sys.excepthook


def my_exception_hook(exectype, value, traceback):
    print(exectype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook


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


class MainWindow(QtWidgets.QMainWindow, win1):
    # Set all initial selected values to None
    selectedHeader = [None] * 3
    selectedOrderNumber = None
    selectedCustomerName = None
    currentTab = 0

    loadedTab = [False] * 3

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        # load all the data into the tables

        login_dialog = login.FirstWindow()
        login_dialog.exec_()

        if not login_dialog.signedIn:
            sys.exit(0)

        self.setupUi(self)
        self.refresh_tab(0)

        if not login_dialog.administrator:
            self.addUserButton.hide()

        # hide help text
        self.helpWidget.hide()

        # Get the header view from the stock table and connect it for when the section is clicked
        stock_table: QTableWidget = self.find_stock_table()
        stock_header: QHeaderView = stock_table.horizontalHeader()
        stock_header.sectionClicked.connect(self.header_section_clicked)

        # Get the header view from the customer table and connect it for when the section is clicked
        customer_table: QTableWidget = self.find_customer_table()
        customer_header: QHeaderView = customer_table.horizontalHeader()
        customer_header.sectionClicked.connect(self.header_section_clicked)

        # Get the header view from the headers table and connect it for when the section is clicked
        headers_table: QTableWidget = self.find_headers_table()
        headers_horizontal_header: QHeaderView = headers_table.horizontalHeader()
        headers_horizontal_header.sectionClicked.connect(self.header_section_clicked)
        headers_vertical_header: QHeaderView = headers_table.verticalHeader()
        headers_vertical_header.sectionClicked.connect(self.vertical_header_section_clicked)

        lines_table: QTableWidget = self.find_lines_table()
        lines_header: QHeaderView = lines_table.horizontalHeader()
        lines_header.sectionClicked.connect(self.header_section_clicked)

    def refresh_tab(self, tabNumber: int):

        # check tab has not been loaded
        if not self.loadedTab[tabNumber]:
            # load data for the relevant table
            if tabNumber == 0:
                self.refresh_stock()
            elif tabNumber == 1:
                self.refresh_customers()
            elif tabNumber == 2:
                self.refresh_header()
            # set that tab to loaded
            self.loadedTab[tabNumber] = True
            # update current tab number
            self.currentTab = tabNumber
        else:
            self.currentTab = tabNumber

    def refresh_column(self, results, column, table, size, numeric=False, price=False):

        # Set the table to column to the size passed into the function
        table.setColumnWidth(column, size)

        # Set the row to the length of results
        row_count: int = len(results)
        table.setRowCount(row_count)

        # Set the starting index to 0
        row_index: int = 0

        if not price:
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
        else:
            for row in results:
                # Set the item in the table to being the name
                number = [self.get_price(x) for x in row][0]

                table.setItem(row_index, column, NumericTableWidgetItem(number))
                row_index = row_index + 1

    def get_price(self, number):
        if number is None:
            pass
        else:
            price = str("{0:.2f}".format(number))
            return price

    def header_section_clicked(self, logicalIndex: int):

        # Find the relevant table and selected header
        if self.currentTab == 0:
            table: QTableWidget = self.find_stock_table()
            selected_header = self.selectedHeader[0]
        elif self.currentTab == 1:
            table: QTableWidget = self.find_customer_table()
            selected_header = self.selectedHeader[1]
        else:
            table: QTableWidget = self.find_headers_table()
            selected_header = self.selectedHeader[2]

        header: QHeaderView = table.horizontalHeader()

        # Check if the table is currently sorted in ascending order and if so sort in descending order
        if selected_header != logicalIndex:
            table.sortItems(logicalIndex, QtCore.Qt.AscendingOrder)
            # Change indicator on the header
            header.setSortIndicator(logicalIndex, QtCore.Qt.AscendingOrder)
            # set selectedHeader to the new selected header index
            selected_header = logicalIndex
        else:
            table.sortItems(logicalIndex, QtCore.Qt.DescendingOrder)
            # Change indicator on the header
            header.setSortIndicator(logicalIndex, QtCore.Qt.DescendingOrder)
            # reset selectedHeader as the column is currently sorted in descending order
            selected_header = None

        # show indicator so clear it is clear to the user how it is sorted
        header.setSortIndicatorShown(True)

        # return the update selected header
        self.selectedHeader[self.currentTab] = selected_header

    def find_stock_table(self) -> QObject:

        # Find the stock table widget
        tab = self.findChild(QTabWidget, "tabWidget")
        stock_tab = tab.findChild(QWidget, "stockTab")
        table = stock_tab.findChild(QTableWidget, "stockTable")

        return table

    def refresh_stock(self):

        # Find the stock table widget
        table: QTableWidget = self.find_stock_table()
        header: QHeaderView = table.horizontalHeader()

        # Read the data from the database and enter it into the relevant column
        title = datalayer.stock_title(db)
        self.refresh_column(title, 0, table, 150)
        author = datalayer.stock_author(db)
        self.refresh_column(author, 1, table, 150)
        # Set numeric to True for price and quantity
        price = datalayer.stock_list_price(db)
        self.refresh_column(price, 2, table, 50, True, True)
        quantity = datalayer.stock_quantity(db)
        self.refresh_column(quantity, 3, table, 50, True)

        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header.setSortIndicatorShown(False)
        self.selectedHeader[self.currentTab] = None

    def add_stock(self):

        # Open add stock dialog and then refresh stock
        stock_dialog = stockdialog.StockDialog()
        stock_dialog.exec_()
        self.refresh_stock()

    def update_stock(self):
        stock_update = stockupdate.StockUpdate()
        stock_update.exec_()
        self.refresh_stock()

    def find_customer_table(self) -> QObject:
        # Find the customer table widget
        tab = self.findChild(QTabWidget, "tabWidget")
        customer_tab = tab.findChild(QWidget, "customerTab")
        table = customer_tab.findChild(QTableWidget, "customerTable")

        return table

    def refresh_customers(self):
        # Find the customer table widget
        table: QTableWidget = self.find_customer_table()
        header: QHeaderView = table.horizontalHeader()

        # Read the data from the database and enter it into the relevant column
        names = datalayer.customer_name(db)
        self.refresh_column(names, 0, table, 100)
        email = datalayer.customer_email(db)
        self.refresh_column(email, 1, table, 100)
        tel = datalayer.customer_tel(db)
        self.refresh_column(tel, 2, table, 100)
        address = datalayer.customer_address(db)
        self.refresh_column(address, 3, table, 100)
        # Set numeric to true for discount
        discount = datalayer.customer_discount(db)
        self.refresh_column(discount, 4, table, 50, True)
        totalSpent = datalayer.customer_total_spent(db)
        self.refresh_column(totalSpent, 5, table, 50, True, True)

        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header.setSortIndicatorShown(False)
        self.selectedHeader[self.currentTab] = None

    def add_customer(self):

        # Open add customer dialog and then refresh customer
        customer_dialog = customerdialog.CustomerDialog()
        customer_dialog.exec_()
        self.refresh_customers()

    def update_customer(self):
        customer_update = CustomerUpdate()
        customer_update.exec_()
        self.refresh_customers()

    def find_headers_table(self) -> QObject:
        # Find the order headers table widget
        tab = self.findChild(QTabWidget, "tabWidget")
        orders_tab = tab.findChild(QWidget, "ordersTab")
        table = orders_tab.findChild(QTableWidget, "headersTable")

        return table

    def refresh_header(self, lines=False):
        # Find the stock table widget
        headerTable: QTableWidget = self.find_headers_table()
        orderTable: QTableWidget = self.find_lines_table()
        header: QHeaderView = headerTable.horizontalHeader()

        # Read the data from the database and enter it into the relevant column
        customerName = datalayer.order_customer_name(db)
        self.refresh_column(customerName, 0, headerTable, 100)
        deliveryAddress = datalayer.order_delivery_address(db)
        self.refresh_column(deliveryAddress, 1, headerTable, 100)
        # Set numeric True for delivery charge
        deliveryCharge = datalayer.order_delivery_charge(db)
        self.refresh_column(deliveryCharge, 2, headerTable, 75, True, True)
        date = datalayer.order_date(db)
        self.refresh_column(date, 3, headerTable, 75)
        totalCost = datalayer.order_cost(db)
        self.refresh_column(totalCost, 4, headerTable, 45, True, True)
        # Set orderNumber column size to zero so it cant be seen
        orderNumber = datalayer.order_number(db)
        self.refresh_column(orderNumber, 5, headerTable, 0)

        headerTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        header.setSortIndicatorShown(False)
        self.selectedHeader[self.currentTab] = None

        # only clear lines if refresh button is clicked
        if not lines:
            while orderTable.rowCount() > 0:
                orderTable.removeRow(0)
            self.clickHeaderLabel.show()

    def add_header(self):

        # Open add header dialog and then refresh header
        header_dialog = headerdialog.HeaderDialog()
        header_dialog.exec_()
        customerID = header_dialog.customerID
        self.refresh_header()
        datalayer.update_total_spent(db, customerID)

    def vertical_header_section_clicked(self, logicalindex: int):
        headersTable: QTableWidget = self.find_headers_table()

        # find Order Number that has been selected
        self.selectedOrderNumber = headersTable.item(logicalindex, 5).text()
        self.selectedCustomerName = headersTable.item(logicalindex, 0).text()

        self.clickHeaderLabel.hide()
        # refresh the OrderLines for relevant order number
        self.refresh_order_lines()

    def refresh_order_lines(self):
        linesTable: QTableWidget = self.find_lines_table()

        # repeat the function for each column
        bookName = datalayer.order_book_name(db, self.selectedOrderNumber)
        self.refresh_column(bookName, 0, linesTable, 200)

        # Set numeric as true so it can be sorted correctly
        quantity = datalayer.order_quantity(db, self.selectedOrderNumber)
        self.refresh_column(quantity, 1, linesTable, 100, True)
        lineCost = datalayer.order_line_cost(db, self.selectedOrderNumber)
        self.refresh_column(lineCost, 2, linesTable, 103, True, True)

        linesTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def find_lines_table(self) -> QObject:
        # Find the order headers table widget
        tab = self.findChild(QTabWidget, "tabWidget")
        orders_tab = tab.findChild(QWidget, "ordersTab")
        table = orders_tab.findChild(QTableWidget, "linesTable")

        return table

    def add_lines(self):
        if self.selectedOrderNumber is not None:
            line_dialog = linedialog.LineDialog(self.selectedOrderNumber, self.selectedCustomerName)
            line_dialog.exec_()
            self.refresh_order_lines()

            customerID = datalayer.find_customer_id(db, self.selectedCustomerName)

            # call refresh header but dont clear lines table
            self.refresh_header(True)
            datalayer.update_total_spent(db, customerID)

    def add_user(self):
        user_dialog = adduser.UserDialog()
        user_dialog.exec_()

    def help(self):
        self.helpWidget.show()

    def close_help(self):
        self.helpWidget.hide()


def main():
    # Handle high resolution displays:
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    window1 = MainWindow(None)
    window1.show()
    app.exec_()


if __name__ == '__main__':
    main()
