import tkinter as tk
from tkinter import ttk
import Login_GUI
import GUI
import multiprocessing

LARGE_FONT= ("Ubuntu", 12)

class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (MainMenu, WarningPage, Login_GUI.LoginPage):
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
 
        
        
class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller.geometry("1280x720")#fix
        controller.title("Sudoku")#fix
        label = tk.Label(self, text="Main Menu", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        sudoku = multiprocessing.Process(target=GUI.main)
        button1 = tk.Button(self, text="Start a New Game", command= sudoku.start())
        button1.pack()
        button2 = tk.Button(self, text="Game Table")
        button2.pack()
        button3 = tk.Button(self, text="Quit", command=quit)
        button3.pack()


if __name__ == "__main__":
    app = Window()
    app.mainloop()