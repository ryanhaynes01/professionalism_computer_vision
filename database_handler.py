import sqlite3 as sql

standard = {"ID": "",
            "Name": "",
            "Address": "",
            "username": "",
            "password": "",
            "Age": 0,
            "DoB": "",
            "Weekly Hours": 0.0,
            "Hierarchy": 0,
            "Face Image": "Base64 string"
}

def init_database(path):
    db = sql.connect(path)
    cur = db.cursor()

    return cur, db
    
def add_to_database(data, cur, command=None):
    if command is not None:
        cur.execute(command)
        return
    
    # add iterative adding of data


if __name__ == '__main__':
    path = "database/database.db"
    cur, db = init_database(path)
    #add_to_database("", cur, """CREATE TABLE Main
    #(ID integer, Name text, Address text, username text, password text, Age integer, DoB text, Weekly Hours real, Hierarchy integer, Face Image text)""")
    #cur.execute("""INSERT INTO Main VALUES ('0001', 'Ryan Haynes', '21 Queen Street', 'ryanhaynes01', 'kekw', 20, '11/06/2001', 10, 0, 'Empty')""")
    #db.commit()
    for row in cur.execute("""SELECT * FROM Main"""):
        print(row)
