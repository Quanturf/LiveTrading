
import sqlite3

db = sqlite3.connect('D:/Alpaca/4_streaming/ticks.db')

c = db.cursor()

#check all table names
c.execute("SELECT name from sqlite_master where type = 'table' ")
c.fetchall()

#check the table structure for a given table
c.execute("PRAGMA table_info(AAPL)")
c.fetchall()

#fetch rows from a table
c.execute("SELECT * FROM AAPL WHERE price > 134.5")
c.fetchall()