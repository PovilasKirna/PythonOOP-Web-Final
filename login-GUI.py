import tkinter as tk
from functools import partial
import db_connector as dbc


class Window():
    def __init__(self, dimensionX, dimensionY, title, LoginManager):
        self.tkWindow = tk.Tk()
        self.tkWindow.geometry(dimensionX + 'x' + dimensionY)
        self.tkWindow.title(title)
        self.createWidgets()
        self.LoginManager = LoginManager
        self.tkWindow.mainloop()

    def validateLogin(self, username, password):
        Username = username.get()
        Password = password.get()
        print("Username: ", Username,
              "\n",
              "Password: ", Password)
        UserList = self.LoginManager.returnQueryList("SELECT Username, Passwd FROM {}")
        for it in UserList:
            if Username == it[0] and Password == it[1]:
                self.tkWindow.quit()

        return

    def createWidgets(self):
        # username label and text entry box
        usernameLabel = tk.Label(
            self.tkWindow, text="User Name").grid(row=0, column=0)
        username = tk.StringVar()
        usernameEntry = tk.Entry(
            self.tkWindow, textvariable=username).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = tk.Label(
            self.tkWindow, text="Password").grid(row=1, column=0)
        password = tk.StringVar()
        passwordEntry = tk.Entry(
            self.tkWindow, textvariable=password, show='*').grid(row=1, column=1)

        ValidateLogin = partial(self.validateLogin, username, password)

        # login button
        loginButton = tk.Button(
            self.tkWindow, text="Login", command=ValidateLogin).grid(row=4, column=0)


if __name__ == "__main__":
    LoginManager = dbc.DbConnector("UserLoginData")
    Window("400", "150", "Sudoku - login", LoginManager)
