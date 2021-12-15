import json
import tkinter as tk
from tkinter import  ttk
from tkinter import font
from tkinter.constants import CENTER, E, EW, NSEW, W

def _from_rgb(rgb):
    
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

class Menu(ttk.Frame):
    def __init__(self, master=None):
        """INIT FOR MENU BASE CLASS"""
        super().__init__(master)
        
        # class variable declaration
        self.frame = ttk.Frame(master, padding=10)
        self.configure_style_info()
        self.colours = ['#5865F2', '#F2A358']
        self.lbl_objs = []
        self.btn_objs = []
        self.txt_objs = []
        self.frame.grid()
        self.row_counter = 0

    def configure_style_info(self):
        """CONFIGURE STYLE TO RUN THROUGH WHOLE GUI"""
        # get font and configure it for all self. objects
        fnt = font.Font(family='Helvetica', size=14, weight="bold")
        self.style = ttk.Style(root)
        self.style = self.style.configure(".", font=fnt)

    def set_options(self, options):
        """SET OPTIONS FOR BUTTONS"""
        self.options = options
        self.init_options()

    def set_labels(self, label):
        """SET LABELS"""
        self.labels = label
        self.init_labels()

    def init_options(self):
        """SEND BUTTON NAMES AND COMMANDS TO BE CREATED"""
        # add the quit button to the botton of the row of buttons
        btn = ttk.Button(self.frame, text="Quit", command=self.master.destroy)
        btn.grid(column=0, row=len(self.options) + len(self.labels))
        self.btn_objs.append(btn)

        # iterate through all options, extracting the tupled command and text information
        for option, cmd in self.options:
            self.add_button(option, cmd)
            self.row_counter += 1

    def init_labels(self):
        """SEND LABEL INFO TO BE CREATED"""
        for label in self.labels:
            self.add_label(label)
            self.row_counter += 1

    def add_label(self, text):
        """CREATE LABELS"""
        lbl = ttk.Label(self.frame, text=f"{text}", wraplength=300, anchor='center')
        lbl.grid(row=self.row_counter, column=0)
        if text.lower() in ["username:", "password:"]:
            self.add_text_box()
        self.lbl_objs.append(lbl)

    def add_button(self, text, cmd):
        """CREATE BUTTONS ASSIGNING THEIR COMMANDS"""
        # create a button object on the master root, assigning text, commands, and position
        btn = ttk.Button(self.frame, text=f"{text}", command=function_mapping[cmd])
        btn.grid(row=self.row_counter, column=0)
        self.btn_objs.append(btn)

    def add_text_box(self):
        #self.row_counter 
        print(self.row_counter)
        txt = ttk.Entry(self.master, font=self.style, width=50)
        txt.grid(row=self.row_counter, column=1, sticky=EW)
        self.txt_objs.append(txt)

    def reset(self):
        """CLEAR THE ROOT FRAME"""
        for lbl in self.lbl_objs:
            lbl.destroy()
        
        for btn in self.btn_objs:
            btn.destroy()

        for txt in self.txt_objs:
            txt.destroy()

class UserInterface(Menu):
    def __init__(self, master=None):
        super().__init__(master)

    # TODO:
    # Create Design for Menus
    # Create Admin Menus
    # Create Employee Menus
    # Add functionality for admin
    # Add functionality for employees


# create the root for the GUI window
# then set the size of the window
# and then instantiate the menu object
root = tk.Tk()
root.geometry("600x300")
root.configure(background='#5865F2')
main = Menu(root)

def load_data(dir):
    """LOAD DISPLAY DATA"""
    # load in display and command data from design jsons
    with open(f"bin/designs/{dir}.json") as f:
        data = json.load(f)
    return data

def create_menu(path):
    # get desired data from certain path
    data = load_data(path)

    # set the title from data
    main.master.title(data['title'])

    # ORDER IS IMPORTANT HERE
    # set the labels first because the buttons should come
    # underneath. Then we call to set options

    # extract label data, if it exists
    if "labels" in data.keys():
        # extract options information from data
        labels = [text for text in data['labels']]
        if 'Username:' in labels:
            print("pog")
        main.set_labels(labels)

    # extract options data, if it exists
    if "buttons" in data.keys():
        # set the option information to the GUI
        main.set_options([(name, command) for name, command in data['buttons']])

    main.row_counter = 0


def main_menu():
    # clear GUI for new items
    main.reset()

    # set the name for the main menu json file
    file_name = "main_menu"

    # configure the columns for single line menus
    main.master.columnconfigure(0, weight=1)

    # add all information to GUI
    create_menu(file_name)

def admin_menu():
    print("We called admin menu!")

def employee_menu():
    print("We called employee menu!")

def login_menu():
    main.reset()

    file_name = "login"

    main.columnconfigure(0, weight=3)

    create_menu(file_name)

def consent_menu():
    # clear GUI for new items
    main.reset()

    # set the name for the consent menu json
    file_name = "consent_menu"

    # set the columnconfigure
    main.master.columnconfigure(0, weight=3)

    # add all information to GUI
    create_menu(file_name)

# function mapper to assign functions to buttons when
# the buttons are created
function_mapping = {
    'consent': login_menu,
    'admin': admin_menu,
    'employee': employee_menu
}

if __name__ == '__main__':
    # initially set up the consent menu
    consent_menu()
    #main.add_text_box()
    # run the root mainloop
    main.mainloop()
