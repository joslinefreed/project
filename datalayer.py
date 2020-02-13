import sqlite3 as lite


def CustomerDetails(db):
    sql = '''
    SELECT Name, Email, Tel, Address, Discount  
    FROM Customer
    '''
    results = sql_command(db, sql)
    return results


def CustomerName(db):
    sql = '''
    SELECT Name 
    FROM Customer
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

def sql_command(db, command, commit=False):
    con = lite.connect(db)
    cur = con.cursor()
    cur.execute(command)
    if commit:
        con.commit()
    results = cur.fetchall()
    results.insert(0, [desc[0] for desc in cur.description])
    return results


def sql_add(db, data, command):
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        cur.execute(command, data)
        con.commit()
    pass


def output_response(response):
    for row in response:
        print('\t'.join([str(x) for x in row]))
