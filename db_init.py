import sqlite3 as sql

con = sql.connect("test.db")
cursor = con.cursor()

sql = """
create table data
(
    girox   double,
    giroy   double,
    giroz   double
)
"""

cursor.execute("insert into data values(12.3, 14.5, 16.5)")

cursor.execute(sql)