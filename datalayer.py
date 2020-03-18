import sqlite3 as lite


def stock_title(db, sort=False):
    sql = '''
    SELECT Title
    FROM Stock
    '''

    if sort:
        sql = '''
        SELECT Title 
        FROM Stock
        ORDER BY 1
        '''

    results = sql_command(db, sql)
    return results


def stock_author(db):
    sql = '''
    SELECT Author
    FROM Stock
    '''
    results = sql_command(db, sql)
    return results


def stock_list_price(db):
    sql = '''
    SELECT ListPrice
    FROM Stock
    '''
    results = sql_command(db, sql)
    return results


def stock_quantity(db):
    sql = '''
    SELECT Quantity
    FROM Stock
    '''
    results = sql_command(db, sql)
    return results


def customer_details(db):
    sql = '''
    SELECT Name, Email, Tel, Address, Discount  
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def customer_name(db, sort=False):
    sql = '''
    SELECT Name 
    FROM Customer
    '''

    if sort:
        sql = '''
        SELECT Name 
        FROM Customer
        ORDER BY 1
        '''

    results = sql_command(db, sql)
    return results


def customer_email(db):
    sql = '''
    SELECT Email
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def customer_tel(db):
    sql = '''
    SELECT Tel
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def customer_address(db):
    sql = '''
    SELECT Address
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def customer_discount(db):
    sql = '''
    SELECT Discount
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def customer_total_spent(db):
    sql = '''
        SELECT TotalSpent
        FROM Customer
        '''
    results = sql_command(db, sql)
    return results


def order_customer(db):
    sql = '''
    SELECT CustomerID
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def order_customer_name(db):
    sql = '''
    SELECT Customer.Name
    FROM OrderHeader
    INNER JOIN Customer
    ON OrderHeader.CustomerID = Customer.CustomerID
    '''
    results = sql_command(db, sql)
    return results


def order_delivery_address(db):
    sql = '''
    SELECT DeliveryAddress
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def order_delivery_charge(db):
    sql = '''
    SELECT DeliveryCharge
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def order_date(db):
    sql = '''
    SELECT OrderDate
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def order_cost(db):
    sql = '''
    SELECT TotalCost
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def order_number(db):
    sql = '''
    SELECT OrderNumber
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def order_book_name(db, number):
    sql = '''
    SELECT Stock.Title
    FROM OrderLines
    INNER JOIN Stock
    ON OrderLines.StockCode = Stock.StockID
    WHERE OrderNumber = ?
    '''
    results = sql_findall(db, number, sql)
    return results


def order_quantity(db, orderNumber):
    sql = '''
    SELECT Quantity
    FROM OrderLines
    WHERE OrderNumber = ?
    '''
    results = sql_findall(db, orderNumber, sql)
    return results


def order_line_cost(db, number):
    sql = '''
    SELECT LinePrice
    FROM OrderLines
    WHERE OrderNumber = ?
    '''
    results = sql_findall(db, number, sql)
    return results


def find_stock_code(db, title):
    sql = '''
    SELECT StockID
    FROM Stock
    WHERE Title = ?
    '''
    results = sql_find(db, title, sql)
    return results


def find_customer_id(db, name):
    sql = '''
    SELECT CustomerID
    FROM Customer
    WHERE Name = ?
    '''
    results = sql_find(db, name, sql)
    return results


def find_stock_price(db, ID):
    sql = '''
    SELECT ListPrice
    FROM Stock
    WHERE StockID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def find_author(db, ID):
    sql = '''
    SELECT Author
    FROM Stock
    WHERE StockID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def find_stock_quantity(db, ID):
    sql = '''
    SELECT Quantity
    FROM Stock
    WHERE StockID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def find_discount(db, name):
    sql = '''
    SELECT Discount
    FROM Customer
    WHERE Name = ?
    '''
    results = sql_find(db, name, sql)
    return results


def find_address(db, ID):
    sql = '''
    SELECT Address
    FROM Customer
    WHERE CustomerID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def find_customer_email(db, ID):
    sql = '''
    SELECT Email
    FROM Customer
    WHERE CustomerID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def find_customer_tel(db, ID):
    sql = '''
    SELECT Tel
    FROM Customer
    WHERE CustomerID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def find_customer_address(db, ID):
    sql = '''
    SELECT Address
    FROM Customer
    WHERE CustomerID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def find_customer_discount(db, ID):
    sql = '''
    SELECT Discount
    FROM Customer
    WHERE CustomerID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def find_administrator(db, ID):
    sql = '''
    SELECT Administrator
    FROM Users
    WHERE UserName = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def add_customer_details(db, data):
    sql = '''
    INSERT INTO Customer (Name, Email, Tel, Address, Discount, TotalSpent)
    VALUES(?, ?, ?, ?, ?, ?)'''
    sql_add(db, data, sql)


def add_stock_details(db, data):
    sql = '''
    INSERT INTO Stock (Title, Author, ListPrice, Quantity)
    VALUES(?, ?, ?, ?)'''
    sql_add(db, data, sql)


def add_header_details(db, data):
    sql = '''
    INSERT INTO OrderHeader (CustomerID, DeliveryAddress, DeliveryCharge, OrderDate, TotalCost)
    VALUES(?, ?, ?, ?, ?)'''
    sql_add(db, data, sql)


def add_line_details(db, data):
    sql = '''
    INSERT INTO OrderLines (OrderNumber, StockCode, Quantity, LinePrice)
    VALUES(?, ?, ?, ?)'''
    sql_add(db, data, sql)


def add_user(db, data):
    sql = '''
    INSERT INTO Users (UserName, Password, Administrator)
    VALUES(?, ?, ?)'''
    sql_add(db, data, sql)


def update_order_cost(db, number):
    sql = '''
    UPDATE OrderHeader
    SET TotalCost =(
    OrderHeader.DeliveryCharge +(
    SELECT SUM(OrderLines.LinePrice) FROM OrderLines WHERE OrderLines.OrderNumber = OrderHeader.OrderNumber))
    WHERE OrderHeader.OrderNumber = ?
    '''
    sql_update(db, number, sql)


def update_total_spent(db, ID):
    sql = '''
    UPDATE Customer
    SET TotalSpent =(
    SELECT sum(OrderHeader.TotalCost) FROM OrderHeader WHERE OrderHeader.CustomerID = Customer.CustomerID)
    WHERE Customer.CustomerID = ?
    '''
    sql_update(db, ID, sql)


def update_author(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET Author = "''' + data + '''"
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def update_stock_price(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET ListPrice = ''' + data + '''
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def update_quantity(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET Quantity = ''' + data + '''
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def update_author(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET Author = "''' + data + '''"
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def update_email(db, data, ID):
    if data is None:
        sql = ('''
          UPDATE Customer
          SET Email = NULL
          WHERE Customer.CustomerID = ?
          ''')
    else:
        sql = ('''
        UPDATE Customer
        SET Email = "''' + data + '''"
        WHERE Customer.CustomerID = ?
        ''')
    sql_update(db, ID, sql)


def update_tel(db, data, ID):
    if data is None:
        sql = ('''
          UPDATE Customer
          SET Tel = NULL
          WHERE Customer.CustomerID = ?
          ''')
    else:
        sql = ('''
        UPDATE Customer
        SET Tel = "''' + data + '''"
        WHERE Customer.CustomerID = ?
        ''')
    sql_update(db, ID, sql)


def update_address(db, data, ID):
    if data is None:
        sql = ('''
          UPDATE Customer
          SET Address = NULL
          WHERE Customer.CustomerID = ?
          ''')
    else:
        sql = ('''
        UPDATE Customer
        SET Address = "''' + data + '''"
        WHERE Customer.CustomerID = ?
        ''')
    sql_update(db, ID, sql)


def update_discount(db, data, ID):
    sql = ('''
    UPDATE Customer
    SET Discount = ''' + data + '''
    WHERE Customer.CustomerID = ?
    ''')
    sql_update(db, ID, sql)


def reduce_quantity(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET Quantity = (Quantity - ''' + data + ''' )
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def check_login(db, name):
    sql = '''
    SELECT Password
    FROM Users
    WHERE UserName = ?
    '''
    results = sql_find(db, name, sql)
    return results


def sql_command(db, command, commit=False):
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute(command)
    if commit:
        con.commit()
    results = cur.fetchall()
    return results


def sql_add(db, data, command):
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        cur.execute(command, data)
        con.commit()


def sql_find(db, data, command):
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute(command, (data,))
    results = cur.fetchone()
    if results is None:
        return False
    else:
        return results[0]


def sql_findall(db, data, command):
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute(command, (data,))
    results = cur.fetchall()
    return results


def sql_update(db, data, command):
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        cur.execute(command, (data,))
        con.commit()


'''update OrderHeader
set TotalCost =(
OrderHeader.DeliveryCharge +(
SELECT sum(OrderLines.LinePrice) from OrderLines where OrderLines.OrderNumber = OrderHeader.OrderNumber)
)'''

'''    
update Customer
set TotalSpent =(
SELECT sum(OrderHeader.TotalCost) from OrderHeader where OrderHeader.CustomerID = Customer.CustomerID)'''
    
'''update OrderHeader
set TotalCost =(
OrderHeader.DeliveryCharge +(
SELECT sum(OrderLines.LinePrice) from OrderLines where OrderLines.OrderNumber = OrderHeader.OrderNumber)
)'''
