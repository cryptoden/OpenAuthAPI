import sqlite3

# TO-DO: For user submitted fields, calculator placeholders automatically

class db:
    def __init__(self, dbFile):
        global conn, cursor
        conn = sqlite3.connect(dbFile, isolation_level=None) # isolation_level=None turns on autocommits, execute statements are written immediately.
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

    def selectOne(self, table, parameter, pData):
        return(cursor.execute('SELECT * FROM '+table+' WHERE '+parameter+' = (?)', [pData]).fetchone()) # Placeholders can only substitute values, not columns or tables.  Make sure columns+table strings do not contain any sql statements.

    def insertOne(self, table, valueList, *fieldList): #value list is (?, ?, ?), number of ? corrosponding to number of fields in the Table.
        cursor.execute('INSERT INTO '+table+' VALUES '+valueList, fieldList[0])

    def updateOne(self, table, parameter, pData, wParameter, wData):
        cursor.execute('UPDATE '+table+' SET '+parameter+'=(?) WHERE '+wParameter+'=(?)', [pData, wData])
