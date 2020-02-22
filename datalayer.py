import sqlite3 as lite


def CustomerDetails(db):
    sql = '''
    SELECT Name, Email, Tel, Address, Discount  
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def CustomerName(db, sort=False):
    sql = '''
    SELECT Name 
    FROM Customer
    '''

    if (sort):
        sql = '''
        SELECT Name 
        FROM Customer
        ORDER BY 1
        '''

    results = sql_command(db, sql)
    return results


def CustomerEmail(db):
    sql = '''
    SELECT Email
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def CustomerTel(db):
    sql = '''
    SELECT Tel
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def CustomerAddress(db):
    sql = '''
    SELECT Address
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def CustomerDiscount(db):
    sql = '''
    SELECT Discount
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results

    # convert the values to integers
    #discounts = []
    #for row in results:
    #    for x in row:
    #        if x is None:
    #            discounts.append(x)
    #        else:
    #            discounts.append(int(x))
    #return discounts


def StockTitle(db):
    sql = '''
    SELECT Title
    FROM Stock
    '''
    results = sql_command(db, sql)
    return results


def StockAuthor(db):
    sql = '''
    SELECT Author
    FROM Stock
    '''
    results = sql_command(db, sql)
    return results


def StockListPrice(db):
    sql = '''
    SELECT ListPrice
    FROM Stock
    '''
    results = sql_command(db, sql)
    return results


def StockQuantity(db):
    sql = '''
    SELECT Quantity
    FROM Stock
    '''
    results = sql_command(db, sql)
    return results


def OrderCustomer(db):
    sql = '''
    SELECT CustomerID
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def OrderCustomerName(db):
    sql = '''
    SELECT Customer.Name
    FROM OrderHeader
    INNER JOIN Customer
    ON OrderHeader.CustomerID = Customer.CustomerID
    '''
    results = sql_command(db, sql)
    return results


def OrderDeliveryAddress(db):
    sql = '''
    SELECT DeliveryAddress
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def OrderDeliveryCharge(db):
    sql = '''
    SELECT DeliveryCharge
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def OrderDate(db):
    sql = '''
    SELECT OrderDate
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def OrderNumber(db):
    sql = '''
    SELECT OrderNumber
    FROM OrderHeader
    '''
    results = sql_command(db, sql)
    return results


def OrderBookName(db, orderNumber):
    sql = '''
    SELECT Stock.Title
    FROM OrderLines
    INNER JOIN Stock
    ON OrderLines.StockCode = Stock.StockID
    WHERE OrderNumber = ?
    '''
    results = sql_findall(db, orderNumber, sql)
    return results


def OrderQuantity(db, orderNumber):
    sql = '''
    SELECT Quantity
    FROM OrderLines
    WHERE OrderNumber = ?
    '''
    results = sql_findall(db, orderNumber, sql)
    return results


def findStockCode(db, name):
    sql = '''
    SELECT StockID
    FROM Stock
    WHERE Title = ?
    '''
    results = sql_find(db, name, sql)
    return results


def findCustomerID(db, name):
    sql = '''
    SELECT CustomerID
    FROM Customer
    WHERE Name = ?
    '''
    results = sql_find(db, name, sql)
    return results


def AddCustomerDetails(db, data):
    sql = '''
    INSERT INTO Customer (Name, Email, Tel, Address, Discount)
    VALUES(?, ?, ?, ?, ?)'''
    sql_add(db, data, sql)
    pass


def AddStockDetails(db, data):
    sql = '''
    INSERT INTO Stock (Title, Author, ListPrice, Quantity)
    VALUES(?, ?, ?, ?)'''
    sql_add(db, data, sql)
    pass


def AddHeaderDetails(db, data):
    sql = '''
    INSERT INTO OrderHeader (CustomerID, DeliveryAddress, DeliveryCharge, OrderDate)
    VALUES(?, ?, ?, ?)'''
    sql_add(db, data, sql)
    pass


def AddLineDetails(db, data):
    sql = '''
    INSERT INTO OrderLines (OrderNumber, StockCode, Quantity)
    VALUES(?, ?, ?)'''
    sql_add(db, data, sql)
    pass


def AddStockDetails(db, data):
    sql = '''
    INSERT INTO Stock (Title, Author, ListPrice, Quantity)
    VALUES(?, ?, ?, ?)'''
    sql_add(db, data, sql)
    pass


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
    pass


def sql_find(db, data, command):
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute(command, (data,))
    results = cur.fetchone()
    return results[0]


def sql_findall(db, data, command):
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute(command, (data,))
    results = cur.fetchall()
    return results


def output_response(response):
    for row in response:
        print('\t'.join([str(x) for x in row]))
