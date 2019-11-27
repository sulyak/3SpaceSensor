import sqlite3 as sql

con = sql.connect("test.db")
cursor = con.cursor()

for row in cursor.execute("select * from data"):
    print(row)