import base64
import utilities as util
import authenticator as auth
import os
import facial_detection as fd
import database_handler as dh
import tkinter as tk
import tkinter.font as tkFont
from tkinter.messagebox import showinfo
import time
import threading
from PIL import Image, ImageTk

def root_clear(root):
    for element in root.winfo_children():
        element.destroy()
    return root

def _from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

class StaffForm:
    def __init__(self, root, hierarchy=1, edit=False, data=None):
        self._root = root
        self._data = data
        self._text_fields = []
        self.edit = edit
        self._fm = util.FileManager()
        self.db = dh.DatabaseHandler()
        self._hierarchy = hierarchy
        root.title("Staff Form")
        root.geometry("450x350")
        ft = tkFont.Font(family='Times',size=12)

        TitleLabel=tk.Label(
            root, bg="#ff8c00", fg="#333333", borderwidth="2px", justify="left",
            anchor="center", relief="flat", text="Staff Form", font=ft
        ).place(x=50,y=10,width=340,height=30)

        NameLabel=tk.Label(
            root, bg="#86e6e7", fg="#333333", font=ft, borderwidth="2px",
            anchor="w", justify="left", relief="flat", text="Name:"
        ).place(x=50,y=45,width=340,height=30)

        NameText=tk.Entry(root, bg="#ffffff", fg="#333333", font=ft)
        NameText.place(x=190,y=45,width=200,height=30)
        self._text_fields.append(NameText)

        AddressLabel=tk.Label(
            root, bg="#86e6e7", fg="#333333", borderwidth="2px", font=ft, 
            justify="left", anchor="w", relief="flat", text="Address:"
        ).place(x=50, y=80, width=340, height=30)

        AddressText=tk.Entry(root, bg="#ffffff", fg="#333333", font=ft)
        AddressText.place(x=190, y=80, width=200, height=30)
        self._text_fields.append(AddressText)

        UsernameLabel=tk.Label(
            root, bg="#86e6e7", fg="#333333", borderwidth="2px", font=ft,
            justify="left", anchor="w", relief="flat", text="Username:"
        ).place(x=50,y=115,width=340,height=30)

        UsernameText=tk.Entry(root, bg="#ffffff", fg="#333333", font=ft)
        UsernameText.place(x=190,y=115,width=200,height=30)
        self._text_fields.append(UsernameText)

        PasswordLabel=tk.Label(
            root, bg="#86e6e7", fg="#333333", borderwidth="2px", font=ft,
            justify="left", anchor="w", relief="flat", text="Password:"
        ).place(x=50,y=150,width=340,height=30)

        PasswordText=tk.Entry(root, bg="#ffffff", fg="#333333", show="*", font=ft)
        PasswordText.place(x=190,y=150,width=200,height=30)
        self._text_fields.append(PasswordText)

        AgeLabel=tk.Label(
            root, bg="#86e6e7", fg="#333333", borderwidth="2px", 
            font=ft, justify="left", anchor="w", text="Age:", relief="flat"
        ).place(x=50,y=185,width=340,height=30)

        AgeText=tk.Entry(root, bg="#ffffff", fg="#333334", font=ft)
        AgeText.place(x=190,y=185,width=200,height=30)
        self._text_fields.append(AgeText)

        DoBLabel=tk.Label(
            root, bg="#86e6e7", fg="#333333", borderwidth="2px", font=ft,
            justify="left", anchor="w", text="Date of Birth", relief="flat"
        ).place(x=50,y=220,width=340,height=30)

        DoBText=tk.Entry(root, bg="#ffffff", fg="#333333", font=ft)
        DoBText.place(x=190,y=220,width=200,height=30)
        self._text_fields.append(DoBText)

        WeeklyHoursLabel=tk.Label(
            root, bg="#86e6e7", fg="#333333", borderwidth="2px", font=ft,
            justify="left", anchor="w", text="Weekly Hours:", relief="flat"
        ).place(x=50,y=255,width=340,height=30)

        WeeklyHoursText=tk.Entry(root, bg="#ffffff", fg="#333333", font=ft)
        WeeklyHoursText.place(x=190,y=255,width=200,height=30)
        self._text_fields.append(WeeklyHoursText)

        BackButton=tk.Button(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text="Back")
        BackButton.place(x=50,y=290,width=100,height=25)
        BackButton["command"] = self.BackButton_command

        SubmitButton=tk.Button(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text="Submit")
        SubmitButton.place(x=290,y=290,width=100,height=25)
        SubmitButton["command"] = self.SubmitButton_command

        if edit:
            self.edit_user()

    def BackButton_command(self):
        self._root.destroy()

    def SubmitButton_command(self):
        if self.edit:
            self.submit_edit()
            return
        
        info = "NULL,"
        for field in self._text_fields:
            if field["fg"] == "#333334":
                info += f"{field.get()},"
            else:
                info += f"'{field.get()}',"
        info += "'1'"
        self.db.handler("insert", [info])
        showinfo("Success", "Information added successfully!")
        self._root.destroy()

    def submit_edit(self):
        fields = list(dh.standard.keys())
        fields.remove(fields[0])
        info, output = "", ""
        for field in self._text_fields:
            if field["fg"] == "#333334":
                info += f"{field.get()},"
            else:
                info += f"{field.get()},"
        info += str(self._hierarchy)
        info = [info]
        info = info[0].split(",")
        for i in range(0, len(fields)):
            if i != len(fields) - 1:
                output += f"{fields[i]} = '{info[i]}',"
            else:
                output += f"{fields[i]} = '{info[i]}'"

        try:
            self.db.handler("edit", [output, f"(ID == {self._data[0]})"])
            self._fm.change_name(self._data[1], info[0])
            self._root.destroy()
        
        except Exception as e:
            print(f"Unknown Error Occured: {e}")
        

    def edit_user(self):
        temp_data = self._data.copy()
        temp_data.remove(temp_data[0])
        temp_data.pop()
        for i in range(0, len(temp_data)):
            self._text_fields[i].insert(0, str(temp_data[i]))


class AdminMenu:
    def __init__(self, root, user):
        self.db = dh.DatabaseHandler()
        #setting title
        self._root = root
        root.title("Admin Menu")
        #setting window size
        width=550
        height=450
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        #root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times',size=12)

        EditEmployee_button=tk.Button(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text="Edit Employee")
        EditEmployee_button.place(x=40,y=220,width=170,height=40)
        EditEmployee_button["command"] = self.edit_employee

        RemoveEmployee_button=tk.Button(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text="Remove Employee")
        RemoveEmployee_button.place(x=40,y=160,width=170,height=40)
        RemoveEmployee_button["command"] = self.remove_employee

        AddEmployee_button=tk.Button(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text="Add Employee")
        AddEmployee_button.place(x=40,y=100,width=170,height=40)
        AddEmployee_button["command"] = self.add_employee

        LogOut_button=tk.Button(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text="Log Out")
        LogOut_button.place(x=40,y=340,width=170,height=40)
        LogOut_button["command"] = self.log_out

        Update_button=tk.Button(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text="Refresh Employees")
        Update_button.place(x=40,y=280,width=170,height=40)
        Update_button["command"] = self.find_employees

        Greeting_label=tk.Label(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text=f"Hello, {user}")
        Greeting_label.place(x=40,y=40,width=170,height=40)

        Employees_listbox=tk.Listbox(root, bg="#ff8c00", fg="#333333", font=ft, borderwidth="1px", justify="center")
        Employees_listbox.place(x=240,y=40,width=260,height=300)
        self._employee_listbox = Employees_listbox

        self.find_employees()

    def find_employees(self):
        self._employee_listbox.delete(0, "end")
        employees = self.db.handler("get", ["Name", "Hierarchy == 1"])
        for employee in employees:
            self._employee_listbox.insert("end", employee[0])

    def edit_employee(self):
        index = -1
        for i in self._employee_listbox.curselection():
            index = i
        
        if index != -1:
            person = self._employee_listbox.get(index)
            data = self.db.get_user("*", "Name", person)
            if data != []:
                temp_root = tk.Tk()
                temp_root["bg"] = self._root["bg"]
                StaffForm(temp_root, 1, True, list(data[0]))

    def remove_employee(self):
        index = -1

        for i in self._employee_listbox.curselection():
            index = i

        if index != -1:
            self.db.remove_user("Name", self._employee_listbox.get(index))
            showinfo("Removed", "Successfully Removed Employee")

    def add_employee(self):
        temp_root = tk.Tk()
        temp_root["bg"] = self._root["bg"]
        StaffForm(temp_root)

    def log_out(self):
        self._root = root_clear(self._root)
        showinfo("Sign Off", "You have been signed out!")
        ConsentMenu(self._root)
        return


class EmployeeMenu:
    def __init__(self, root, name):
        #setting title
        self._root = root
        self.db = dh.DatabaseHandler()
        root.title("Employee Menu")
        #setting window size
        width=550
        height=450
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        ft = tkFont.Font(family='Times',size=12)

        EditInfo=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Edit Information")
        EditInfo.place(x=40,y=220,width=170,height=40)
        EditInfo["command"] = self.GButton_562_command

        ClockOut=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Clock Out")
        ClockOut.place(x=40,y=160,width=170,height=40)
        ClockOut["command"] = self.GButton_923_command

        ClockIn=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Clock In")
        ClockIn.place(x=40,y=100,width=170,height=40)
        ClockIn["command"] = self.GButton_351_command

        LogOut=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Log Out")
        LogOut.place(x=40,y=280,width=170,height=40)
        LogOut["command"] = self.log_out

        EmployeeName=tk.Label(root, bg="#ff8c00", fg="#000000", font=ft, justify="center", text=f"Hello, {name}")
        EmployeeName.place(x=40,y=40,width=170,height=40)

        InfoBox=tk.Listbox(root, bg="#ff8c00", fg="#333333", borderwidth="1px", font=ft, justify="center")
        InfoBox.place(x=240,y=40,width=260,height=300)
        self._info_list = InfoBox

        self.get_info(name)

    def GButton_562_command(self):
        print("command")


    def GButton_923_command(self):
        print("command")


    def GButton_351_command(self):
        print("command")


    def GButton_141_command(self):
        print("command")


    def log_out(self):
        self._root = root_clear(self._root)
        showinfo("Sign Off", "You have been signed out!")
        ConsentMenu(self._root)
        return

    def get_info(self, name):
        fields = list(dh.standard.keys())
        person = name
        data = self.db.handler("get", ["*", f"Name == '{person}'"])
        if data != []:
            data = data[0]
            for i in range(0, len(fields)):
                self._info_list.insert(tk.END, f"{fields[i].title()}: {data[i]}")


class ConsentMenu:
    def __init__(self, root):
        #setting title
        self._root = root
        root.title("Consent Menu")        
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root["bg"] = "#1e9fff"
        ft = tkFont.Font(family='Times',size=10)

        TnCsLabel=tk.Label(root, anchor="center", bg="#ff8c00", font=ft, fg="#333333", justify="left")
        self.TnCsLabel=TnCsLabel
        TnCsLabel["text"] = """
        By using this program
        you are consenting to the usage and
        storage of your face. If you
        do not consent to the usage of
        your face, please manually login to the
        program. However, if you
        do consent to the usage of this information, 
        please press the consent button and login
        using the camera."""
        TnCsLabel.place(x=140,y=60,width=280,height=150)
        
        LoginManButton=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Login Manually")
        LoginManButton.place(x=120,y=280,width=100,height=25)
        LoginManButton["command"] = self.LoginManButton_command

        ExitButton=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Exit")
        ExitButton.place(x=340,y=280,width=100,height=25)
        ExitButton["command"] = self.ExitButton_command


        ConsentCheckBox=tk.Checkbutton(root, font=ft, bg="#ff8c00", fg="#333333", justify="center", text="Consent", offvalue="0", onvalue="1")
        self.ConsentCheckBox=ConsentCheckBox
        ConsentCheckBox.place(x=140,y=220,width=70,height=25)
        ConsentCheckBox["command"] = self.ConsentCheckBox_command

        LoginButton=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Continue to Login", state="disabled")
        LoginButton.place(x=230,y=280,width=100,height=25)
        LoginButton["command"] = self.LoginButton_command
        self.LoginButton=LoginButton

    def LoginManButton_command(self):
        self._root = root_clear(self._root)
        ManualLogin(self._root)

    def ExitButton_command(self):
        self._root.destroy()
        return

    def ConsentCheckBox_command(self):
        if self.LoginButton["state"] == "normal":
            self.LoginButton["state"] = "disabled"
        else:
            self.LoginButton["state"] = "normal"

    def LoginButton_command(self):
        self._root = root_clear(self._root)
        LoginWithVideo(self._root)

class ManualLogin:
    def __init__(self, root):
        self.db = dh.DatabaseHandler()
        self._root = root
        #setting title
        root.title("Login Screen")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        #root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times',size=12)

        UserLabel=tk.Label(root, bg="#86e6e7", borderwidth="2px", font=ft, anchor="w", fg="#333333", justify="left", text="Username: ", relief="flat")
        UserLabel.place(x=120,y=130,width=340,height=30)

        UserText=tk.Entry(root, bg="#ffffff", font=ft, fg="#333333")
        UserText.place(x=260,y=130,width=200,height=30)
        self._user_text = UserText

        PassLabel=tk.Label(root, bg="#86e6e7", borderwidth="2px", font=ft, fg="#333333", justify="left", anchor="w", text="Password:", relief="flat")
        PassLabel.place(x=120,y=180,width=340,height=30)

        PassText=tk.Entry(root, bg="#ffffff", show="*", font=ft, fg="#333333")
        PassText.place(x=260,y=180,width=200,height=30)
        self._pass_text = PassText

        BackButton=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Back")
        BackButton.place(x=120,y=220,width=100,height=25)
        BackButton["command"] = self.BackButton_command

        LoginButton=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Continue")
        LoginButton.place(x=360,y=220,width=100,height=25)
        LoginButton["command"] = self.LoginButton_command

    def BackButton_command(self):        
        self._root = root_clear(self._root)
        ConsentMenu(self._root)

    def LoginButton_command(self):
        username = self._user_text.get()
        password = self._pass_text.get()
        authenticator = auth.Authenticator()
        # details structure: varification (bool), hierarchy (int), name (string)
        details = authenticator.users_info("username, password", "username", username, password)

        try:
            if not details[0]:
                showinfo("Login Error", "Invalid Details")
                self._root = root_clear(self._root)
                ManualLogin(self._root)
                return

            showinfo("Logged In", "You have successfully logged in!")
            if details[1] == 0:
                self._root = root_clear(self._root)
                AdminMenu(self._root, details[2])
                return
            else:
                self._root = root_clear(self._root)
                EmployeeMenu(self._root, details[2])
                return

        except TypeError as e:
            pass

class LoginWithVideo():
    def __init__(self, root):
        self._root = root
        self._root.title("Face Login")
        self.face = fd.FacialDetection()
        self.db = dh.DatabaseHandler()
        self.thread = threading.Thread(target=self.face.show_video, args=())
        self.frame = None
        self._username_error = False
        ft = tkFont.Font(family='Times',size=12)

        UserLabel=tk.Label(root, bg="#86e6e7", borderwidth="2px", font=ft, anchor="w", fg="#333333", justify="left", text="Username: ", relief="flat")
        UserLabel.place(x=120,y=130,width=340,height=30)

        UserText=tk.Entry(root, bg="#ffffff", font=ft, fg="#333333")
        UserText.place(x=260,y=130,width=200,height=30)
        self._user_text = UserText

        BackButton=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Back")
        BackButton.place(x=120,y=170,width=100,height=25)
        BackButton["command"] = self.BackButton_command

        LoginButton=tk.Button(root, bg="#ff8c00", font=ft, fg="#000000", justify="center", text="Continue")
        LoginButton.place(x=360,y=170,width=100,height=25)
        LoginButton["command"] = self.LoginButton_command

    def authenticator(self, name):
        details = {
            "hierarchy": 0
        }

        details_tuple = self.db.get_user("Hierarchy", "Name", name)

        for key in details.keys():
            details[key] = details_tuple[0][details[key]]

        return details

    def get_name_and_encoded(self, username):
        try:
            # get the users name from the database
            name = self.db.get_user("Name", "username", username)
            name = name[0][0]

            # try to open their face data
            with open(f"faces/{name}/encoded.bin", "rb", buffering=0) as f:
                image_to_decode = f.read()

            # decode to string
            image = base64.b64decode(image_to_decode)

            # load the image into image data, this is the temp object
            # that fd will use to know who to find
            with open(f"faces/{name}/tmp.jpg", "wb") as f:
                f.write(image)

            # tell fd where to find the image
            self.face.temp_location = f"faces/{name}/tmp.jpg"

            return name
        
        except IndexError:
            showinfo("Username Error", f"Invalid Username: {username}")
            return None

        except Exception as e:
            print(e)
            return None

    def init_user_data(self, name):
        try:
            # load the encodings data
            self.face.load_encodings()

            # now that the data is set, we can start
            # the thread and tell fd the name of the
            # person that it's looking for
            self.thread.start()
            self.face.known_face_names[0] = name

        except Exception as e:
            print(e)

    def view_video(self, username):
        try:
            self._root = root_clear(self._root)
            name = self.get_name_and_encoded(username)
            
            if name is None:
                raise NameError("Invalid Username")

            self.label = tk.Label(self._root, text="Camera is starting...")
            self.label["font"] = tkFont.Font(family="Times", size=20)
            self.label.grid(row=0, column=0)
            self._root.update()

            self.init_user_data(name)
        
            os.remove(f"faces/{name}/tmp.jpg")

        except NameError as e:
            print(e)
            LoginWithVideo(self._root)
            return

        except Exception as e:
            print(e)
            LoginWithVideo(self._root)
            return

        while self.thread.is_alive():
            if self.face.public_frame is not None:
                if self.face.init_time is None:
                    self.face.init_time = time.time()
            
                self.frame = self.face.public_frame
                image = Image.fromarray(self.frame)
                image = ImageTk.PhotoImage(image)

                if self.label is None:
                    self.label["image"] = image
                    self.label.grid(row=0, column=0)
                else:
                    self.label["image"] = image

                self._root.update()

        if self.face.is_found:
            self._root = root_clear(self._root)
            details = self.authenticator(name)
            if details["hierarchy"] == 0:
                AdminMenu(self._root, name)
                return
            else:
                EmployeeMenu(self._root, name)
                return
        else:
            #for element in self._root.winfo_children():
            #    element.destory
            self.label.destroy()
            self._root.update()
            showinfo("Error", f"Couldn't identify {name}")
            ConsentMenu(self._root)

    def LoginButton_command(self):
        username = self._user_text.get()
        self.view_video(username)

    def BackButton_command(self):
        self._root = root_clear(self._root)
        ConsentMenu(self._root)


def main():
    # create the root for the GUI window
    # then set the size of the window
    # and then instantiate the menu object
    root = tk.Tk()
    root.configure(background='#5865F2')
    # initially set up the consent menu
    ConsentMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()