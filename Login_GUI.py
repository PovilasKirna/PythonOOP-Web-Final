import tkinter as tk
from functools import partial
import db_connector as dbc
import Main_GUI as mm


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        controller.geometry("400x150")
        controller.title("Sudoku - Login")
        self.LoginManager = dbc.DbConnector("UserLoginData")
        self.controller = controller
        self.createWidgets()

    def validateLogin(self, username, password):
        Username = username.get()
        Password = password.get()
        UserList = self.LoginManager.returnQueryList("SELECT Username, Passwd FROM {}")
        for it in UserList:
            if Username == it[0] and Password == it[1]:
                print("Success")
                self.controller.show_frame("MainMenu")
                return True
        print("Bad details")
        return False

    def createWidgets(self):
        # username label and text entry box
        usernameLabel = tk.Label(self, text="User Name").grid(row=0, column=0)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = tk.Label(self, text="Password").grid(row=1, column=0)
        password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable=password, show='*').grid(row=1, column=1)
        
        # login button
        loginButton = tk.Button(self, text="Login", command=lambda: self.validateLogin(username, password)).grid(row=4, column=0)
        
        quitbutton = tk.Button(self, text="Cancel", command=quit).grid(row=4, column=1, sticky="w")
