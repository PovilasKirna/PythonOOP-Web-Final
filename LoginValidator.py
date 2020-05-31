import tkinter as tk
from functools import partial
import db_connector as dbc
import Main_GUI as mm


class Login(tk.Frame):
    def __init__(self):
        self.LoginManager = dbc.DbConnector("UserLoginData")        

    def validateLogin(self, username, password):
        UserList = self.LoginManager.returnQueryList("SELECT Username, Passwd FROM {}")
        for it in UserList:
            if username == it[0] and password == it[1]:
                print("Successfully validated")
                return True
        print("Bad details")
        return False