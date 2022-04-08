import base64
import sys
import os
import database_handler as dh

class FileManager():
    def __init__(self):
        # establish the current working directory
        # for the rest of the manager to use
        self.cwd = os.getcwd()
    
    def change_name(self, old_name, new_name):
        # get the path for all of the face data
        # then find the path for the old name, and what the new
        # path will look like after the name has been altered
        face_path = self.create_path(self.cwd, "faces")
        old_path = self.create_path(face_path, old_name)
        new_path = self.create_path(face_path, new_name)

        try:
            # validate all of the paths and then rename the directory
            self.validate_path(old_path)
            os.rename(old_path, new_path)
            self.validate_path(new_path)

        except OSError as e:
            # TODO:
            # log data to an appropriate file

            # throw the error raised to the console
            print(e)

    def validate_path(self, dir):
        # tell the program if the directory exists, so we
        # we can proceed with execution
        if os.path.exists(dir):
            return True
        
        # get the traceback if something went wrong and raise it
        traceback = sys.exc_info()[2]
        raise FileNotFoundError(
            f"File/Directory could not be found:\n{dir}"
        ).with_traceback(traceback)
    
    def create_path(self, path=None, *args):
        # if no base path is provided, work from the current working directory
        if path is None:
            path = os.getcwd()

        # append each child folder in args to the path, geenerating a long
        # directory string to be used
        for child in args:
            path = os.path.join(path, child)

        return path

class ImageEncoder():
    def __init__(self, name):
        self._name = name

    def convert(self):
        with open(f"faces/{self._name}/face.jpg", "rb") as f:
            converted = base64.b64encode(f.read())

        with open(f"faces/{self._name}/encoded.bin", "wb") as f:
            f.write(converted)

def main():
    fields = list(dh.standard.keys())
    fields.remove(fields[0])
    print(fields)
    test = ["'Alexandros Aspiotis','Maybe In The Bin','alexasp','alex',23,'2/6/1998','10.0','1','Empty'"]
    test = test[0].split(",")
    print(test)
    output = ""
    for i in range(0, len(fields)):
        output += f"{fields[i]} = {test[i]},"

    print(output)

if __name__ == '__main__':
    #main()
    fm = FileManager()
    fm.change_name("Alex Tuckeradsf", "Alex Tucker")