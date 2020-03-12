import sqlite3 as lite


def StockTitle(db, sort=False):
    sql = '''
    SELECT Title
    FROM Stock
    '''

    if (sort):
        sql = '''
        SELECT Title 
        FROM Stock
        ORDER BY 1
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

    if sort:
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


def CustomerTotalSpent(db):
    sql = '''
        SELECT TotalSpent
        FROM Customer
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


def OrderCost(db):
    sql = '''
    SELECT TotalCost
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


def OrderBookName(db, number):
    sql = '''
    SELECT Stock.Title
    FROM OrderLines
    INNER JOIN Stock
    ON OrderLines.StockCode = Stock.StockID
    WHERE OrderNumber = ?
    '''
    results = sql_findall(db, number, sql)
    return results


def OrderQuantity(db, orderNumber):
    sql = '''
    SELECT Quantity
    FROM OrderLines
    WHERE OrderNumber = ?
    '''
    results = sql_findall(db, orderNumber, sql)
    return results


def OrderLineCost(db, number):
    sql = '''
    SELECT LinePrice
    FROM OrderLines
    WHERE OrderNumber = ?
    '''
    results = sql_findall(db, number, sql)
    return results


def findStockCode(db, title):
    sql = '''
    SELECT StockID
    FROM Stock
    WHERE Title = ?
    '''
    results = sql_find(db, title, sql)
    return results


def findCustomerID(db, name):
    sql = '''
    SELECT CustomerID
    FROM Customer
    WHERE Name = ?
    '''
    results = sql_find(db, name, sql)
    return results


def findStockPrice(db, ID):
    sql = '''
    SELECT ListPrice
    FROM Stock
    WHERE StockID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def findAuthor(db, ID):
    sql = '''
    SELECT Author
    FROM Stock
    WHERE StockID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def findStockQuantity(db, ID):
    sql = '''
    SELECT Quantity
    FROM Stock
    WHERE StockID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def findDiscount(db, name):
    sql = '''
    SELECT Discount
    FROM Customer
    WHERE Name = ?
    '''
    results = sql_find(db, name, sql)
    return results


def findAddress(db, ID):
    sql = '''
    SELECT Address
    FROM Customer
    WHERE CustomerID = ?
    '''
    results = sql_find(db, ID, sql)
    return results


def AddCustomerDetails(db, data):
    sql = '''
    INSERT INTO Customer (Name, Email, Tel, Address, Discount, TotalSpent)
    VALUES(?, ?, ?, ?, ?, ?)'''
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
    INSERT INTO OrderHeader (CustomerID, DeliveryAddress, DeliveryCharge, OrderDate, TotalCost)
    VALUES(?, ?, ?, ?, ?)'''
    sql_add(db, data, sql)
    pass


def AddLineDetails(db, data):
    sql = '''
    INSERT INTO OrderLines (OrderNumber, StockCode, Quantity, LinePrice)
    VALUES(?, ?, ?, ?)'''
    sql_add(db, data, sql)
    pass


def UpdateOrderCost(db, number):
    sql = '''
    UPDATE OrderHeader
    SET TotalCost =(
    OrderHeader.DeliveryCharge +(
    SELECT SUM(OrderLines.LinePrice) FROM OrderLines WHERE OrderLines.OrderNumber = OrderHeader.OrderNumber))
    WHERE OrderHeader.OrderNumber = ?
    '''
    sql_update(db, number, sql)
    pass


def UpdateTotalSpent(db, ID):
    sql = '''
    UPDATE Customer
    SET TotalSpent =(
    SELECT sum(OrderHeader.TotalCost) FROM OrderHeader WHERE OrderHeader.CustomerID = Customer.CustomerID)
    WHERE Customer.CustomerID = ?
    '''
    print(ID)
    sql_update(db, ID, sql)


def UpdateAuthor(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET Author = ''' + data + '''
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def UpdateStockPrice(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET ListPrice = ''' + data + '''
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def UpdateQuantity(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET Quantity = ''' + data + '''
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def ReduceQuantity(db, data, ID):
    sql = ('''
    UPDATE Stock
    SET Quantity = (Quantity - ''' + data + ''' )
    WHERE Stock.StockID = ?
    ''')
    sql_update(db, ID, sql)


def checkLogin(db, name):
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
    pass


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
    pass


'''update OrderHeader
set TotalCost =(
OrderHeader.DeliveryCharge +(
SELECT sum(OrderLines.LinePrice) from OrderLines where OrderLines.OrderNumber = OrderHeader.OrderNumber)
)'''

'''    
update Customer
set TotalSpent =(
SELECT sum(OrderHeader.TotalCost) from OrderHeader where OrderHeader.CustomerID = Customer.CustomerID
)
    
update OrderHeader
set TotalCost =(
OrderHeader.DeliveryCharge +(
SELECT sum(OrderLines.LinePrice) from OrderLines where OrderLines.OrderNumber = OrderHeader.OrderNumber)
)'''
