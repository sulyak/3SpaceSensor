import sqlite3 as sql

def main():
    con = sql.connect("test.db")
    cursor = con.cursor()
    init(con)

    for row in cursor.execute("select * from data"):
        print(row)

    con.close()

def init(con):
    cursor = con.cursor()

    query = """
    create table if not exists data
    (
        giro0x   double,
        giro0y   double,
        giro0z   double,
        accel0x  double,
        accel0y  double,
        accel0z  double,
        comp0x   double,
        comp0y   double,
        comp0z   double
    )
    """
    cursor.execute(query)
    cursor.execute("insert into data values(12.3, 14.5, 16.5, 17.0, 0, 0, 0, 0, 0)")
    cursor.execute("insert into data values(11.3, 13.5, 15.5, 0, 0, 0, 0, 0, 0)")
    cursor.execute("insert into data values(10.3, 12.5, 14.5, 0, 0, 0, 0, 0, 0)")
    remove_duplicated(con)
    con.commit()

def remove_duplicated(con):
    cursor = con.cursor()
    """
    CREATE TABLE temp_table as SELECT DISTINCT * FROM data;
    DELETE FROM data; 
    INSERT INTO data SELECT * FROM temp_table;
    DROP temp_table
    """
    cursor.execute("CREATE TABLE if not exists temp_table as SELECT DISTINCT * FROM data")
    cursor.execute("DELETE FROM data")
    cursor.execute("INSERT INTO data SELECT * FROM temp_table")
    cursor.execute("DROP table temp_table")

    con.commit()

if __name__ == "__main__": main()