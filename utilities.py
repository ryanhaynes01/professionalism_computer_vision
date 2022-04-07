import base64
import sys
import os
import database_handler as dh

class FileManager():
    def __init__(self):
        cwd = os.getcwd()
        self.face_path = os.path.join(cwd, "faces")
    
    def change_name(self, old_name, new_name):
        old_path = os.path.join(self.face_path, old_name)
        new_path = os.path.join(self.face_path, new_name)

        try:
            os.rename(old_path, new_path)
        except OSError:
            traceback = sys.exc_info()[2]
            raise FileNotFoundError(
                "Original path does not exist. The name provided might be wrong"
            ).with_traceback(traceback)

    def validate_path(self, dir):
        if os.path.exists(dir):
            return True
        
        raise FileNotFoundError("File/Directory could not be found")
    
    def create_path(self, *args):
        path = os.getcwd()
        for child in args:
            path = os.path.join(path, child)

        return path

class ImageEncoder():
    def __init__(self, name):
        self.name = name

    def convert(self):
        with open(f"faces/{self.name}/face.jpg", "rb") as f:
            converted = base64.b64encode(f.read())

        with open(f"faces/{self.name}/encoded.bin", "wb") as f:
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
    try:
        fm = FileManager()
        fm.change_name("Alex Tuckeradsf", "Alex Tucker")
    except Exception as e:
        print(e)