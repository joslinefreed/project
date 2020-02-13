
#import sqlite3 as lite


def main():
    '''db = 'Book Selling Database.db'
    CustomerName(db)
    ID = int(input("Find the stock with ID: "))
    StockTitle(db,ID)'''

'''
    colorButton = QtWidgets.QPushButton("Colors")
    clickMeAct = QtWidgets.QAction('Click Me', self)
    clickMeAct.triggered.connect(lambda action: print("I was clicked!"))
    readDataAct = QtWidgets.QAction('ReadData', self)
    readDataAct.triggered.connect(lambda action: self.my_read())

    toolbar = self.addToolBar("MyToolBar")

    toolbar.addWidget(colorButton)
    toolbar.addAction(clickMeAct)
    toolbar.addAction(readDataAct)

    menu = QtWidgets.QMenu()
    menu.addAction("red")
    menu.addAction("green")
    menu.addAction("blue")
    colorButton.setMenu(menu)

    menu.triggered.connect(lambda action: print(action.text()))
'''



#def CustomerName(db):
#    sql = '''
#    SELECT Name
#    FROM Customer
#    '''
#    results = sql_command(db, sql)
#    output_response(results)
#
#def StockTitle(db,ID):
#    sql = '''
#    SELECT Title
#    FROM Stock
#    WHERE StockID = '2';
#    '''
#    results = sql_command(db, sql)
#    output_response(results)
#
#
#def sql_command(db, command, commit=False):
#    con = lite.connect(db)
#    cur = con.cursor()
#    cur.execute(command)
#    if commit:
#        con.commit()
#    results = cur.fetchall()
#    results.insert(0, [desc[0] for desc in cur.description])
#    return results


#def CustomerName(db):
#    sql = '''
#    SELECT Name
#    FROM Customer
#    '''
#    results = sql_command(db, sql)
#    return results


#def StockTitle(db, ID):
#    sql = '''
#    SELECT Title
#    FROM Stock
#    WHERE StockID = '2';
#    '''
#    results = sql_command(db, sql)
#    output_response(results)




#def output_response(response):
#    for row in response:
#        print('\t'.join([str(x) for x in row]))
#
#    def my_read(self):
#        print("Reading customer names from the database:")
#
#        db = 'Book Selling Database.db'
#        results = CustomerName(db)
#        for row in results:
#            print('\t'.join([str(x) for x in row]))

#    def refreshCustomers(self):
#        db = 'Book Selling Database.db'
#        results = CustomerName(db)

        # Find the customer table widget
#        tab: QTabWidget = self.findChild(QTabWidget, "tabWidget")
#        first_tab: QWidget = tab.findChild(QWidget, "customerTab")
#        table: QTableWidget = first_tab.findChild(QTableWidget, "customerTable")

        # Clear the table
#        table.clearContents()

        # Set the table row count to be the number of results, excluding the heading row
#        row_count: int = len(results) - 1
#        table.setRowCount(row_count)

#        row_index: int = 0
#        heading_row = True
#        for row in results:
#            if heading_row:
#                # Skip the heading by not adding it
#                heading_row = False
#            else:
#                # Set the item in the table to being the customer name
#                name: str = [str(x) for x in row][0]
#                table.setItem(row_index, 0, QTableWidgetItem(name))
#                row_index = row_index + 1

        # table1 = QTableWidget()
        # table1..clearContents()
        # = first_tab.findChild(, "customerTable")

        # table.

        # tab1.findChild(Q)
        # print(tab.currentTabName)

        # if tab.currentTabName == "tabCustomer":
        #    print("Customer tab is the current one")
        # else:
        #    print(tab.currentTabName)

        # tab.currentWidget()

        # QTabWidget x = QTableWidget()
        # x.setCurrentIndex(0)
        # x.currentIndex()
        # x.current
        # x.currentTabName
        # print(tab)
        # tab.
        # tab1 = tab([)0]
        # tab1 = tab.findChild(QWidget, "customerTab")
        # print(tab1)
        # table = tab.findChild(QTableWidget, "customerTableWidget")
        # print(table)

        # table = self.findChild(QTableWidget, "customerTableWidget")
        # print(table)


if __name__ == '__main__':
    main()


