import base64
import database_handler as dh

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
    main()