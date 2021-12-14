import json
import sqlite3 as sql

def init_database(path):
    db = sql.connect(path)
    cur = db.cursor()

    return cur, db
    

if __name__ == '__main__':
    path = "database/database.db"
    cur, db = init_database(path)
    #cur.execute("""CREATE TABLE test
    #(name text, email text, age real)""")
    #cur.execute("""INSERT INTO test VALUES ('ryan', 'pog@gmail.com', 20)""")
    #db.commit()
    for row in cur.execute("""SELECT * FROM test"""):
        print(row)
