import tkinter as tk
from tkinter import ttk
import LoginValidator
import GUI
import threading

LARGE_FONT= ("Ubuntu", 12)


class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (MainMenu, WarningPage, GameTable, Login_GUI.LoginPage):
            frame = F(container, self)
            instanceName = type(frame).__name__
            self.frames[instanceName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.Alpha = True
        if(self.Alpha):
            self.show_frame("WarningPage")#fix
        else: 
            self.show_frame("LoginPage")#fix
        
    def GetFrames(self):
        return self.frames   
     
    def FrameExists(self, cont):
        frame = self.frames[cont]
        result = False
        if(frame) : result = True
        else : result = False
        return result
 
    def show_frame(self, cont):        
        frame = self.frames[cont]
        frame.tkraise()

        
class WarningPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)       
        controller.geometry("400x150")#fix
        controller.title("Sudoku - Warning")#fix
        label = tk.Label(self, text="WARNING: This is a alpha software \n use at your own risk!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Agree", command=lambda: controller.show_frame("LoginPage"))
        button1.pack()
        button2 = ttk.Button(self, text="Disagree", command=quit)
        button2.pack()
 
class GameTable(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)       
        controller.geometry("1280x720")#fix
        controller.title("Sudoku - Games")#fix
        label = tk.Label(self, text="Your Games", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Go back to menu", command=lambda: controller.show_frame("MainMenu"))
        button1.pack()
        button2 = ttk.Button(self, text="Quit", command=quit)
        button2.pack()
        
class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("1280x720")#fix
        controller.title("Sudoku")#fix
        label = tk.Label(self, text="Main Menu", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = tk.Button(self, text="Start a New Game", command=lambda: self.startGame())
        button1.pack()
        button2 = tk.Button(self, text="Game Table", command=lambda: controller.show_frame("GameTable"))
        button2.pack()
        button3 = tk.Button(self, text="Quit", command=quit)
        button3.pack()
        
    def startGame(self,parent):
        parent.destroy()
        GUI.main()
        



if __name__ == "__main__":
    app = Window()
    app.mainloop()
    