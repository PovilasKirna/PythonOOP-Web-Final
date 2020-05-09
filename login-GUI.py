import tkinter as tk
from functools import partial

class Window():
	def __init__(self, dimensionX, dimensionY, title):
		self.tkWindow = tk.Tk()
		self.tkWindow.geometry(dimensionX + 'x' + dimensionY)
		self.tkWindow.title(title)
		self.createWidgets()
		self.tkWindow.mainloop()

	def validateLogin(self, username, password):
		Username = username.get()
		Password = password.get()
		print("Username: ", Username,
			"\n",
				"Password: ", Password)
		if Username == "Povilas Kirna" and Password == "g0f0ritdude":
			self.tkWindow.quit()

		return

	def createWidgets(self):
		#username label and text entry box
		usernameLabel = tk.Label(self.tkWindow, text="User Name").grid(row=0, column=0)
		username = tk.StringVar()
		usernameEntry = tk.Entry(self.tkWindow, textvariable=username).grid(row=0, column=1)

		#password label and password entry box
		passwordLabel = tk.Label(self.tkWindow,text="Password").grid(row=1, column=0)
		password = tk.StringVar()
		passwordEntry = tk.Entry(self.tkWindow, textvariable=password, show='*').grid(row=1, column=1)

		ValidateLogin = partial(self.validateLogin, username, password)

		#login button
		loginButton = tk.Button(self.tkWindow, text="Login", command=ValidateLogin).grid(row=4, column=0)


Window("400", "150", "Sudoku - login")