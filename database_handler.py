import sqlite3 as sql
import traceback
import sys
import datetime

# standard for adding to the database, with type specific requirements
standard = {
    "ID": bool,
    "Name": str,
    "Address": str,
    "username": str,
    "password": str,
    "Age": int,
    "DoB": str,
    "WeeklyHours": float,
    "Hierarchy": int
}

# general stucture for commands that will be executed on the database
commands = {
    "insert": "INSERT INTO Main VALUES (<arguments>)",
    "remove": "DELETE FROM Main WHERE <condition>",
    "edit": "UPDATE Main SET <condition> WHERE <condition2>",
    "get": "SELECT <arguments> FROM Main WHERE <condition>",
    "view_specific": "SELECT <arguments> FROM Main",
    "view_all": "SELECT * FROM Main" 
}

class DatabaseHandler:
    def __init__(self):
        # initialize all basic database variables, and then connect to the database itself
        self._db = None
        self._cur = None
        self.__path = "database/database.db"
        self.init_database()

    def error_log(self, error, type, value, tb):
        print(f"SQLite Error: {' '.join(error.args)}")
        print(f"Exception Class: {error.__class__}")
        print("SQLite Error Traceback")
        for text in traceback.format_exception(type, value, tb):
            print(text)

        now = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        with open(f"crash/{now}.txt", "x") as f:
            f.writelines(f"SQLite Error: {' '.join(error.args)}")
            f.writelines(f"\nException Class: {error.__class__}")
            f.writelines("\nSQLite Error Traceback:\n")
            for text in traceback.format_exception(type, value, tb):
                f.writelines(text)

    def init_database(self):
        # establish a connection to the database, and assign the database and cursor objects
        try:
            self._db = sql.connect(self.__path)
            self._cur = self._db.cursor()
        except sql.Error as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.error_log(e, (exc_type, exc_value, exc_tb))

    def display_from_database(self, command:str = None):
        # check to make sure that the command actually contains text to be displayed
        if command is None:
            print("Error Displaying, no command given")
            return

        # otherwise, display each row that is produced from the executed command
        for row in self._cur.execute(command):
            print(row)

    def basic_database_commands(self, command:str = None):
        # check to make sure that the command is not empty
        if command is None:
            print("Error executing, no command given")
            return

        # otherwise execute the command and then commit the change
        try:
            if command.__contains__("SELECT"):
                temp = self._cur.execute(command).fetchall()
                return temp
            self._cur.execute(command)
            self._db.commit()
        except sql.Error as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            self.error_log(e, exc_type, exc_value, exc_tb)

    def get_user(self, id, reference, provided):
        info = None
        try:
            info = self.handler("get", [f"{id}", f"{reference} == '{provided}'"])
        
        except Exception as e:
            print(f"handler: {e}")

        return info

    def remove_user(self, id, provided):
        self.handler("remove", [f"{id} == '{provided}'"])

    def handler(self, command:str = None, data:list = []):
        # convert the desired command to lowercase
        command = command.lower()

        # if the command is not in the commands dictionary, it's either
        # not implemented yet or just doesn't exist, so return error
        if command not in commands.keys():
            print(f"Error: {command} doesn't exist")
            return
        
        # get the skeleton of the command from the commands dictionary
        raw_command = commands[command]

        # for each piece of data provided from the list, cutout the <arguments> or <conditions>
        # placements, and replace them with the commands that actually need to be executed
        for i in range(len(data)):
            start = raw_command.find("<")
            end = raw_command.find(">")
            to_replace = raw_command[start:end+1]
            raw_command = raw_command.replace(to_replace, data[i])

        # if view specific, display
        if command == "view_all":
            self.display_from_database(raw_command)
            return

        # otherwise, execute the commands without much visual aid
        temp = self.basic_database_commands(raw_command)
        if temp is not None:
            return temp


if __name__ == '__main__':
    # this is primarily a fallback, so if the database does not currently exist, make one
    #dbh = DatabaseHandler()
    #if dbh._db is None:
    #dbh._cur.execute("""CREATE TABLE Main
    #(ID integer PRIMARY KEY AUTOINCREMENT, Name text NOT NULL, Address text NOT NULL, username text NOT NULL,
    #password text NOT NULL, Age integer NOT NULL, DoB text NOT NULL, WeeklyHours real, Hierarchy integer NOT NULL)""")
    #dbh._db.commit()
    #dbh._cur.execute("""INSERT INTO Main VALUES (NULL, 'Ryan Haynes', '21 Queen Street', 'ryanhaynes01', 'kekw', 20, '11/06/2001', 10, 0)""")
    #db.commit()
    #print(dbh.handler("insert", ["NULL, 'Ryan Haynes', '21 Queen Street', 'ryanhaynes01', 'kekw', 20, '11/06/2001', 10, 0"]))
    #dbh.handler("view_all")
    #handler(["NULL, 'Alex Tucker', 'Somewhere lol', 'atucker', 'pogchamp', 19, 'pog', 0.1, 0, ''"], "insert")
    #face = open("face_test/Ryan/encoded.bin", "rb")
    #face = face.read()
    #face = face.decode("utf-8")
    #dbh.handler("edit", [f"""'Face' = "'{face}'\"""", "ID == 1"])
    #print(dbh.handler("get", ["*", "username == 'ryanhaynes01'"]))
    pass
