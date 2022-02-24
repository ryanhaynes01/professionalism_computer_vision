import base64
import utilities as util
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
        self.db = dh.DatabaseHandler()
        self._hierarchy = hierarchy
        root.title("Staff Form")
        root.geometry("450x350")

        TitleLabel=tk.Label(root)
        TitleLabel["bg"] = "#ff8c00"
        TitleLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        TitleLabel["font"] = ft
        TitleLabel["anchor"] = "center"
        TitleLabel["fg"] = "#333333"
        TitleLabel["justify"] = "left"
        TitleLabel["text"] = "Staff Form!"
        TitleLabel["relief"] = "flat"
        TitleLabel.place(x=50,y=10,width=340,height=30)

        NameLabel=tk.Label(root)
        NameLabel["bg"] = "#86e6e7"
        NameLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        NameLabel["font"] = ft
        NameLabel["anchor"] = "w"
        NameLabel["fg"] = "#333333"
        NameLabel["justify"] = "left"
        NameLabel["text"] = "Name: "
        NameLabel["relief"] = "flat"
        NameLabel.place(x=50,y=45,width=340,height=30)

        NameText=tk.Entry(root)
        self._name_field = NameText
        self._text_fields.append(NameText)
        NameText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        NameText["font"] = ft
        NameText["fg"] = "#333333"
        NameText.place(x=190,y=45,width=200,height=30)

        AddressLabel=tk.Label(root)
        AddressLabel["bg"] = "#86e6e7"
        AddressLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        AddressLabel["font"] = ft
        AddressLabel["fg"] = "#333333"
        AddressLabel["justify"] = "left"
        AddressLabel["anchor"] = "w"
        AddressLabel["text"] = "Address: "
        AddressLabel["relief"] = "flat"
        AddressLabel.place(x=50,y=80,width=340,height=30)

        AddressText=tk.Entry(root)
        self._address_field = AddressText
        self._text_fields.append(AddressText)
        AddressText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        AddressText["font"] = ft
        AddressText["fg"] = "#333333"
        AddressText.place(x=190,y=80,width=200,height=30)

        UsernameLabel=tk.Label(root)
        UsernameLabel["bg"] = "#86e6e7"
        UsernameLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        UsernameLabel["font"] = ft
        UsernameLabel["fg"] = "#333333"
        UsernameLabel["justify"] = "left"
        UsernameLabel["anchor"] = "w"
        UsernameLabel["text"] = "Username: "
        UsernameLabel["relief"] = "flat"
        UsernameLabel.place(x=50,y=115,width=340,height=30)

        UsernameText=tk.Entry(root)
        self._username_field = UsernameText
        self._text_fields.append(UsernameText)
        UsernameText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        UsernameText["font"] = ft
        UsernameText["fg"] = "#333333"
        UsernameText.place(x=190,y=115,width=200,height=30)

        PasswordLabel=tk.Label(root)
        PasswordLabel["bg"] = "#86e6e7"
        PasswordLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        PasswordLabel["font"] = ft
        PasswordLabel["fg"] = "#333333"
        PasswordLabel["justify"] = "left"
        PasswordLabel["anchor"] = "w"
        PasswordLabel["text"] = "Password: "
        PasswordLabel["relief"] = "flat"
        PasswordLabel.place(x=50,y=150,width=340,height=30)

        PasswordText=tk.Entry(root)
        self._password_field = PasswordText
        self._text_fields.append(PasswordText)
        PasswordText["bg"] = "#ffffff"
        PasswordText.config(show="*")
        ft = tkFont.Font(family='Times',size=12)
        PasswordText["font"] = ft
        PasswordText["fg"] = "#333333"
        PasswordText.place(x=190,y=150,width=200,height=30)

        AgeLabel=tk.Label(root)
        AgeLabel["bg"] = "#86e6e7"
        AgeLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        AgeLabel["font"] = ft
        AgeLabel["fg"] = "#333333"
        AgeLabel["justify"] = "left"
        AgeLabel["anchor"] = "w"
        AgeLabel["text"] = "Age: "
        AgeLabel["relief"] = "flat"
        AgeLabel.place(x=50,y=185,width=340,height=30)

        AgeText=tk.Entry(root)
        self._age_field = AgeText
        self._text_fields.append(AgeText)
        AgeText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        AgeText["font"] = ft
        AgeText["fg"] = "#333334"
        AgeText.place(x=190,y=185,width=200,height=30)

        DoBLabel=tk.Label(root)
        DoBLabel["bg"] = "#86e6e7"
        DoBLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        DoBLabel["font"] = ft
        DoBLabel["fg"] = "#333333"
        DoBLabel["justify"] = "left"
        DoBLabel["anchor"] = "w"
        DoBLabel["text"] = "Date of Birth: "
        DoBLabel["relief"] = "flat"
        DoBLabel.place(x=50,y=220,width=340,height=30)

        DoBText=tk.Entry(root)
        self._dob_field = DoBText
        self._text_fields.append(DoBText)
        DoBText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        DoBText["font"] = ft
        DoBText["fg"] = "#333333"
        DoBText.place(x=190,y=220,width=200,height=30)

        WeeklyHoursLabel=tk.Label(root)
        WeeklyHoursLabel["bg"] = "#86e6e7"
        WeeklyHoursLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        WeeklyHoursLabel["font"] = ft
        WeeklyHoursLabel["fg"] = "#333333"
        WeeklyHoursLabel["justify"] = "left"
        WeeklyHoursLabel["anchor"] = "w"
        WeeklyHoursLabel["text"] = "Weekly Hours: "
        WeeklyHoursLabel["relief"] = "flat"
        WeeklyHoursLabel.place(x=50,y=255,width=340,height=30)

        WeeklyHoursText=tk.Entry(root)
        self._weekly_hours_field = WeeklyHoursText
        self._text_fields.append(WeeklyHoursText)
        WeeklyHoursText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        WeeklyHoursText["font"] = ft
        WeeklyHoursText["fg"] = "#333333"
        WeeklyHoursText.place(x=190,y=255,width=200,height=30)

        BackButton=tk.Button(root)
        BackButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        BackButton["font"] = ft
        BackButton["fg"] = "#000000"
        BackButton["justify"] = "center"
        BackButton["text"] = "Back"
        BackButton.place(x=50,y=290,width=100,height=25)

        BackButton["command"] = self.BackButton_command

        SubmitButton=tk.Button(root)
        SubmitButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        SubmitButton["font"] = ft
        SubmitButton["fg"] = "#000000"
        SubmitButton["justify"] = "center"
        SubmitButton["text"] = "Submit"
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

        self.db.handler("edit", [output, f"(ID == {self._data[0]})"])
        self._root.destroy()
        

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

        EditEmployee_button=tk.Button(root)
        EditEmployee_button["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        EditEmployee_button["font"] = ft
        EditEmployee_button["fg"] = "#000000"
        EditEmployee_button["justify"] = "center"
        EditEmployee_button["text"] = "Edit Employee"
        EditEmployee_button.place(x=40,y=220,width=170,height=40)
        EditEmployee_button["command"] = self.edit_employee

        RemoveEmployee_button=tk.Button(root)
        RemoveEmployee_button["bg"] = "#ff7800"
        ft = tkFont.Font(family='Times',size=12)
        RemoveEmployee_button["font"] = ft
        RemoveEmployee_button["fg"] = "#000000"
        RemoveEmployee_button["justify"] = "center"
        RemoveEmployee_button["text"] = "Remove Employee"
        RemoveEmployee_button.place(x=40,y=160,width=170,height=40)
        RemoveEmployee_button["command"] = self.remove_employee

        AddEmployee_button=tk.Button(root)
        AddEmployee_button["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        AddEmployee_button["font"] = ft
        AddEmployee_button["fg"] = "#000000"
        AddEmployee_button["justify"] = "center"
        AddEmployee_button["text"] = "Add Employee"
        AddEmployee_button.place(x=40,y=100,width=170,height=40)
        AddEmployee_button["command"] = self.add_employee

        LogOut_button=tk.Button(root)
        LogOut_button["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        LogOut_button["font"] = ft
        LogOut_button["fg"] = "#000000"
        LogOut_button["justify"] = "center"
        LogOut_button["text"] = "Log Out"
        LogOut_button.place(x=40,y=340,width=170,height=40)
        LogOut_button["command"] = self.log_out

        Update_button=tk.Button(root)
        Update_button["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        Update_button["font"] = ft
        Update_button["fg"] = "#000000"
        Update_button["justify"] = "center"
        Update_button["text"] = "Refresh Employees"
        Update_button.place(x=40,y=280,width=170,height=40)
        Update_button["command"] = self.find_employees

        Greeting_label=tk.Label(root)
        Greeting_label["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        Greeting_label["font"] = ft
        Greeting_label["fg"] = "#000000"
        Greeting_label["justify"] = "center"
        Greeting_label["text"] = f"Hello, {user}"
        Greeting_label.place(x=40,y=40,width=170,height=40)

        Employees_listbox=tk.Listbox(root)
        self._employee_listbox = Employees_listbox
        Employees_listbox["bg"] = "#ff8c00"
        Employees_listbox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        Employees_listbox["font"] = ft
        Employees_listbox["fg"] = "#333333"
        Employees_listbox["justify"] = "center"
        Employees_listbox.place(x=240,y=40,width=260,height=300)

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
            data = self.db.handler("get", ["*", f"Name == '{person}'"])
            if data != []:
                temp_root = tk.Tk()
                temp_root["bg"] = self._root["bg"]
                StaffForm(temp_root, 1, True, list(data[0]))

    def remove_employee(self):
        print("command")

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

        EditInfo=tk.Button(root)
        EditInfo["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        EditInfo["font"] = ft
        EditInfo["fg"] = "#000000"
        EditInfo["justify"] = "center"
        EditInfo["text"] = "Edit Information"
        EditInfo.place(x=40,y=220,width=170,height=40)
        EditInfo["command"] = self.GButton_562_command

        ClockOut=tk.Button(root)
        ClockOut["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        ClockOut["font"] = ft
        ClockOut["fg"] = "#000000"
        ClockOut["justify"] = "center"
        ClockOut["text"] = "Clock Out"
        ClockOut.place(x=40,y=160,width=170,height=40)
        ClockOut["command"] = self.GButton_923_command

        ClockIn=tk.Button(root)
        ClockIn["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        ClockIn["font"] = ft
        ClockIn["fg"] = "#000000"
        ClockIn["justify"] = "center"
        ClockIn["text"] = "Clock In"
        ClockIn.place(x=40,y=100,width=170,height=40)
        ClockIn["command"] = self.GButton_351_command

        LogOut=tk.Button(root)
        LogOut["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        LogOut["font"] = ft
        LogOut["fg"] = "#000000"
        LogOut["justify"] = "center"
        LogOut["text"] = "Log Out"
        LogOut.place(x=40,y=280,width=170,height=40)
        LogOut["command"] = self.log_out

        EmployeeName=tk.Label(root)
        EmployeeName["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=12)
        EmployeeName["font"] = ft
        EmployeeName["fg"] = "#000000"
        EmployeeName["justify"] = "center"
        EmployeeName["text"] = f"Hello, {name}"
        EmployeeName.place(x=40,y=40,width=170,height=40)

        InfoBox=tk.Listbox(root)
        self._info_list = InfoBox
        InfoBox["bg"] = "#ff8c00"
        InfoBox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        InfoBox["font"] = ft
        InfoBox["fg"] = "#333333"
        InfoBox["justify"] = "center"
        InfoBox.place(x=240,y=40,width=260,height=300)

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

        TnCsLabel=tk.Label(root)
        self.TnCsLabel=TnCsLabel
        TnCsLabel["anchor"] = "center"
        TnCsLabel["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        TnCsLabel["font"] = ft
        TnCsLabel["fg"] = "#333333"
        TnCsLabel["justify"] = "left"
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
        
        LoginManButton=tk.Button(root)
        LoginManButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        LoginManButton["font"] = ft
        LoginManButton["fg"] = "#000000"
        LoginManButton["justify"] = "center"
        LoginManButton["text"] = "Login Manually"
        LoginManButton.place(x=120,y=280,width=100,height=25)
        LoginManButton["command"] = self.LoginManButton_command

        ExitButton=tk.Button(root)
        ExitButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        ExitButton["font"] = ft
        ExitButton["fg"] = "#000000"
        ExitButton["justify"] = "center"
        ExitButton["text"] = "Exit"
        ExitButton.place(x=340,y=280,width=100,height=25)
        ExitButton["command"] = self.ExitButton_command


        ConsentCheckBox=tk.Checkbutton(root)
        self.ConsentCheckBox=ConsentCheckBox
        ft = tkFont.Font(family='Times',size=10)
        ConsentCheckBox["font"] = ft
        ConsentCheckBox["bg"] = "#ff8c00"
        ConsentCheckBox["fg"] = "#333333"
        ConsentCheckBox["justify"] = "center"
        ConsentCheckBox["text"] = "Consent"
        ConsentCheckBox.place(x=140,y=220,width=70,height=25)
        ConsentCheckBox["offvalue"] = "0"
        ConsentCheckBox["onvalue"] = "1"
        ConsentCheckBox["command"] = self.ConsentCheckBox_command

        LoginButton=tk.Button(root)
        self.LoginButton=LoginButton
        LoginButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        LoginButton["font"] = ft
        LoginButton["fg"] = "#000000"
        LoginButton["justify"] = "center"
        LoginButton["text"] = "Continue to Login"
        LoginButton.place(x=230,y=280,width=100,height=25)
        LoginButton["command"] = self.LoginButton_command
        LoginButton["state"] = "disabled"

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

        UserLabel=tk.Label(root)
        UserLabel["bg"] = "#86e6e7"
        UserLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        UserLabel["font"] = ft
        UserLabel["anchor"] = "w"
        UserLabel["fg"] = "#333333"
        UserLabel["justify"] = "left"
        UserLabel["text"] = "Username: "
        UserLabel["relief"] = "flat"
        UserLabel.place(x=120,y=130,width=340,height=30)

        UserText=tk.Text(root)
        self._user_text = UserText
        UserText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        UserText["font"] = ft
        UserText["fg"] = "#333333"
        UserText.place(x=260,y=130,width=200,height=30)

        PassLabel=tk.Label(root)
        PassLabel["bg"] = "#86e6e7"
        PassLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        PassLabel["font"] = ft
        PassLabel["fg"] = "#333333"
        PassLabel["justify"] = "left"
        PassLabel["anchor"] = "w"
        PassLabel["text"] = "Password:"
        PassLabel["relief"] = "flat"
        PassLabel.place(x=120,y=180,width=340,height=30)

        PassText=tk.Entry(root)
        self._pass_text = PassText
        PassText["bg"] = "#ffffff"
        PassText.config(show="*")
        ft = tkFont.Font(family='Times',size=12)
        PassText["font"] = ft
        PassText["fg"] = "#333333"
        PassText.place(x=260,y=180,width=200,height=30)

        BackButton=tk.Button(root)
        BackButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        BackButton["font"] = ft
        BackButton["fg"] = "#000000"
        BackButton["justify"] = "center"
        BackButton["text"] = "Back"
        BackButton.place(x=120,y=220,width=100,height=25)

        BackButton["command"] = self.BackButton_command

        LoginButton=tk.Button(root)
        LoginButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        LoginButton["font"] = ft
        LoginButton["fg"] = "#000000"
        LoginButton["justify"] = "center"
        LoginButton["text"] = "Continue"
        LoginButton.place(x=360,y=220,width=100,height=25)

        LoginButton["command"] = self.LoginButton_command

    def BackButton_command(self):        
        self._root = root_clear(self._root)
        ConsentMenu(self._root)
    
    def authenticator(self, username, password):
        details = {
            "hierarchy": 0,
            "name": 1
        }
        info = self.db.handler("get", ["username, password", f"username == '{username}'"])
        if info:
            info = info[0]
            if (info[0] == username and info[1] == password):
                details_tuple = self.db.handler("get", ["Hierarchy, Name", f"username == '{username}'"])
                for key in details.keys():
                    details[key] = details_tuple[0][details[key]]
                return True, details
        
        showinfo("Invalid Details", "Either the username or password were incorrect, please try again")
        return False, details

    def LoginButton_command(self):
        username = self._user_text.get(1.0, "end-1c")
        password = self._pass_text.get()
        logged, details = self.authenticator(username, password)
        if logged:
            showinfo("Logged In", "You have successfully logged in!")
            if details["hierarchy"] == 0:
                self._root = root_clear(self._root)
                AdminMenu(self._root, details["name"])
                return
            else:
                self._root = root_clear(self._root)
                EmployeeMenu(self._root, details["name"])
                return
        
        self._root = root_clear(self._root)
        ManualLogin(self._root)

class LoginWithVideo():
    def __init__(self, root):
        self._root = root
        self._root.title("Face Login")
        self.face = fd.FacialDetection()
        self.db = dh.DatabaseHandler()
        self.thread = threading.Thread(target=self.face.show_video, args=())
        self.frame = None
        self._username_error = False

        UserLabel=tk.Label(root)
        UserLabel["bg"] = "#86e6e7"
        UserLabel["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=12)
        UserLabel["font"] = ft
        UserLabel["anchor"] = "w"
        UserLabel["fg"] = "#333333"
        UserLabel["justify"] = "left"
        UserLabel["text"] = "Username: "
        UserLabel["relief"] = "flat"
        UserLabel.place(x=120,y=130,width=340,height=30)

        UserText=tk.Text(root)
        self._user_text = UserText
        UserText["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=12)
        UserText["font"] = ft
        UserText["fg"] = "#333333"
        UserText.place(x=260,y=130,width=200,height=30)

        BackButton=tk.Button(root)
        BackButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        BackButton["font"] = ft
        BackButton["fg"] = "#000000"
        BackButton["justify"] = "center"
        BackButton["text"] = "Back"
        BackButton.place(x=120,y=170,width=100,height=25)

        BackButton["command"] = self.BackButton_command

        LoginButton=tk.Button(root)
        LoginButton["bg"] = "#ff8c00"
        ft = tkFont.Font(family='Times',size=10)
        LoginButton["font"] = ft
        LoginButton["fg"] = "#000000"
        LoginButton["justify"] = "center"
        LoginButton["text"] = "Continue"
        LoginButton.place(x=360,y=170,width=100,height=25)

        LoginButton["command"] = self.LoginButton_command

    def authenticator(self, name):
        details = {
            "hierarchy": 0
        }

        details_tuple = self.db.handler("get", ["Hierarchy", f"Name == '{name}'"])

        for key in details.keys():
            details[key] = details_tuple[0][details[key]]

        return details

    def get_name_and_encoded(self, username):
        try:
            # get the users name from the database
            name = self.db.handler("get", ["Name", f"username == '{username}'"])[0][0]

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
        
        except Exception as e:
            self._username_error = True
            print(e)

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
        self._root = root_clear(self._root)
        name = self.get_name_and_encoded(username)

        if self._username_error:
            showinfo("Invalid Details", "Sorry, the username entered does not exist!")
            LoginWithVideo(self._root)
            return

        self.label = tk.Label(self._root)
        self.label["font"] = tkFont.Font(family="Times", size=20)
        self.label["text"] = "Camera is starting...."
        self.label.grid(row=0, column=0)
        self._root.update()

        self.init_user_data(name)

        try:
            os.remove(f"faces/{name}/tmp.jpg")
        
        except Exception as e:
            print(e)
            return

        while self.thread.is_alive():
            if self.face.public_frame is not None:
                if self.face.init_time is None:
                    self.face.init_time = time.time()
            
                self.frame = self.face.public_frame
                #image = cv.cvtColor(self.frame, 0, cv.COLOR_BGR2RGB)
                image = Image.fromarray(self.frame)
                image = ImageTk.PhotoImage(image)

                if self.label is None:
                    self.label["image"] = image
                    self.label.grid(row=0, column=0)
                else:
                    self.label["image"] = image

                self._root.update()

        if not self.face.found_camera:
            self.label.destroy()
            showinfo("Camera Error", "The camera could not be accessed")
            ConsentMenu(self._root)
            return

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
        username = self._user_text.get(1.0, "end-1c")
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