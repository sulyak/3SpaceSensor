import sqlite3 as sql

def main():
    con = ("test.db")
    cursor = con.cursor()
    init(con)

    for row in cursor.execute("select * from data"):
        print(row)

    con.close()

def init(db):
    con = sql.connect(db)
    cursor = con.cursor()

    query = """
    create table if not exists data
    (
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        giro0x   double,
        giro0y   double,
        giro0z   double,
        accel0x  double,
        accel0y  double,
        accel0z  double,
        comp0x   double,
        comp0y   double,
        comp0z   double,

        giro1x   double,
        giro1y   double,
        giro1z   double,
        accel1x  double,
        accel1y  double,
        accel1z  double,
        comp1x   double,
        comp1y   double,
        comp1z   double,

        giro2x   double,
        giro2y   double,
        giro2z   double,
        accel2x  double,
        accel2y  double,
        accel2z  double,
        comp2x   double,
        comp2y   double,
        comp2z   double,

        giro3x   double,
        giro3y   double,
        giro3z   double,
        accel3x  double,
        accel3y  double,
        accel3z  double,
        comp3x   double,
        comp3y   double,
        comp3z   double,

        giro4x   double,
        giro4y   double,
        giro4z   double,
        accel4x  double,
        accel4y  double,
        accel4z  double,
        comp4x   double,
        comp4y   double,
        comp4z   double,

        giro5x   double,
        giro5y   double,
        giro5z   double,
        accel5x  double,
        accel5y  double,
        accel5z  double,
        comp5x   double,
        comp5y   double,
        comp5z   double,

        giro6x   double,
        giro6y   double,
        giro6z   double,
        accel6x  double,
        accel6y  double,
        accel6z  double,
        comp6x   double,
        comp6y   double,
        comp6z   double,

        giro7x   double,
        giro7y   double,
        giro7z   double,
        accel7x  double,
        accel7y  double,
        accel7z  double,
        comp7x   double,
        comp7y   double,
        comp7z   double,

        giro8x   double,
        giro8y   double,
        giro8z   double,
        accel8x  double,
        accel8y  double,
        accel8z  double,
        comp8x   double,
        comp8y   double,
        comp8z   double,

        giro9x   double,
        giro9y   double,
        giro9z   double,
        accel9x  double,
        accel9y  double,
        accel9z  double,
        comp9x   double,
        comp9y   double,
        comp9z   double,

        giro10x   double,
        giro10y   double,
        giro10z   double,
        accel10x  double,
        accel10y  double,
        accel10z  double,
        comp10x   double,
        comp10y   double,
        comp10z   double,

        giro11x   double,
        giro11y   double,
        giro11z   double,
        accel11x  double,
        accel11y  double,
        accel11z  double,
        comp11x   double,
        comp11y   double,
        comp11z   double,

        giro12x   double,
        giro12y   double,
        giro12z   double,
        accel12x  double,
        accel12y  double,
        accel12z  double,
        comp12x   double,
        comp12y   double,
        comp12z   double,

        giro13x   double,
        giro13y   double,
        giro13z   double,
        accel13x  double,
        accel13y  double,
        accel13z  double,
        comp13x   double,
        comp13y   double,
        comp13z   double,

        giro14x   double,
        giro14y   double,
        giro14z   double,
        accel14x  double,
        accel14y  double,
        accel14z  double,
        comp14x   double,
        comp14y   double,
        comp14z   double,

        giro15x   double,
        giro15y   double,
        giro15z   double,
        accel15x  double,
        accel15y  double,
        accel15z  double,
        comp15x   double,
        comp15y   double,
        comp15z   double,

        giro16x   double,
        giro16y   double,
        giro16z   double,
        accel16x  double,
        accel16y  double,
        accel16z  double,
        comp16x   double,
        comp16y   double,
        comp16z   double  
    )
    """
    cursor.execute(query)
    remove_duplicated(con)
    con.commit()
    return con

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