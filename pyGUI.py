import pygame
import GUI
import pygameInput as pi
import time
from LoginValidator import Login
from List import ListItem as li
import db_connector as dbc


pygame.init()
#Main variables
display_width = 1280
display_heigth = 720
run = True

#Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (186, 18 ,0)
delete_red = (241, 157, 157)
highlight_delete_red = (244, 200, 200)
play_green = (160, 241, 157)
highlight_play_green = (205, 244, 200)
btn = (157, 209, 241)
highlight_btn = (200, 224, 244)
transparent = (0, 0, 0, 0)
sortImg = (5,151,240)

#Fonts
pygame.font.init()
font = pygame.font.SysFont("robotoregularttf", 40)
font_small = pygame.font.SysFont("robotoregularttf", 24)

#images
playImg = pygame.image.load("icons/play.png")
trashImg = pygame.image.load("icons/trash.png")
sortImg = pygame.image.load("icons/sort.png")
sortNumericUpImg = pygame.image.load("icons/sort-numeric-up.png")
sortNumericDownImg = pygame.image.load("icons/sort-numeric-down.png")
sortAlphaUpImg = pygame.image.load("icons/sort-alpha-up.png")
sortAlphaDownImg = pygame.image.load("icons/sort-alpha-down.png")
sortAmountUpImg = pygame.image.load("icons/sort-amount-up.png")
sortAmountDownImg = pygame.image.load("icons/sort-amount-down.png")
icon = pygame.image.load("icons/icon.png")
pygame.display.set_icon(icon)

class Widgets():
    def __init__(self, window):
        self.window = window
        
    def text(self, text, x, y):
        TextSurf, TextRect = self.text_objects(text, font, black)
        TextRect.center = ((x), (y))
        self.window.blit(TextSurf, TextRect)
        
    def textAllignLeft(self, text, x, y):#bottom left anchor point
        TextSurf, TextRect = self.text_objects(text, font, black)
        TextRect.bottomleft = ((x), (y))
        self.window.blit(TextSurf, TextRect)
        
    def small_text(self, text, x, y):
        TextSurf, TextRect = self.text_objects(text, font_small, black)
        TextRect.center = ((x), (y))
        self.window.blit(TextSurf, TextRect)
        
    def text_objects(self, text, font, color):
        textSurface = font.render(text, 1, color)
        return textSurface, textSurface.get_rect()

    def button(self, msg, font, x,y,w,h,ic,ac, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.window, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
                time.sleep(0.15)
        else:
            pygame.draw.rect(self.window, ic, (x, y, w, h))
        textSurf, textRect = self.text_objects(msg, font, black)
        textRect.center = ( (x+(w/2), y+(h/2)) )
        self.window.blit(textSurf, textRect)
        
class Row():
    def __init__(self, window, index, *args):
        self.window = window
        self.index = index
        self.W = Widgets(self.window)
        self.createRow(*args)
        
    def createRow(self, *args):
        self.sorting("Unsorted")
        name = self.shortenNameToFit(str(args[1][0]))
            
        if self.index <= 3:
            self.W.button("", font, 258, (218+self.index*109), 382, 60, btn, btn)
            self.W.button((str(81-args[1][2])+"/81"), font, 650, (218+self.index*109), 111, 60, btn, btn)
            self.W.button(str(args[1][1]), font, 771, (218+self.index*109), 111, 60, btn, btn)
            self.W.button("", font, 891, (218+self.index*109), 60, 60, play_green, highlight_play_green,lambda: self.loadGame(*args))
            self.W.button("", font, 961, (218+self.index*109), 60, 60, delete_red, highlight_delete_red, lambda: self.deleteRow(*args))
            self.W.textAllignLeft(name, 282, (272+self.index*109))
            self.window.blit(playImg, (905, (230+self.index*109)))
            self.window.blit(trashImg, (978, (230+self.index*109)))
            self.W.button("", font, 258, (302+self.index*109), 763, 1, black, black)#acts like a line
        
    def loadGame(self, *args):
        # print(args)
        # print("playerID:", args[0][0][0], "sudokuID:", args[1][4], "sudokuName:", args[1][0], "time:", args[1][1], "board:", args[1][5])
        pygame.display.quit()
        GUI.loadGame(args[0][0][0],args[1][4], args[1][0], args[1][1], args[1][5])
        
    def deleteRow(self, *args):
        try:
            dbAgent = dbc.DbConnector("Sudoku")
            dbAgent.deleteSudokuGame(args[1][4])
        except:
            self.drawErrorPage()
    
    def sorting(self, sortMethod):
        if sortMethod == "Unsorted":
            self.window.blit(sortImg, (442, 169))
            self.window.blit(sortImg, (699, 169))
            self.window.blit(sortImg, (819, 169))
        elif sortMethod == "Sort by Alpha Up":
            self.window.blit(sortAlphaUpImg, (442, 169))
            self.window.blit(sortImg, (699, 169))
            self.window.blit(sortImg, (819, 169))
        elif sortMethod == "Sort by Alpha Down":
            self.window.blit(sortAlphaDownImg, (442, 169))
            self.window.blit(sortImg, (699, 169))
            self.window.blit(sortImg, (819, 169))
        elif sortMethod == "Sort by Numeric Up":
            self.window.blit(sortImg, (699, 169))
            self.window.blit(sortNumericUpImg, (819, 169))
            self.window.blit(sortImg, (819, 169))
        elif sortMethod == "Sort by Numeric Down":
            self.window.blit(sortImg, (699, 169))
            self.window.blit(sortNumericDownImg, (819, 169))
            self.window.blit(sortImg, (819, 169))
        elif sortMethod == "Sort by Amount Up":
            self.window.blit(sortImg, (699, 169))
            self.window.blit(sortImg, (819, 169))
            self.window.blit(sortAmountUpImg, (699, 169))
        elif sortMethod == "Sort by Amount Down":
            self.window.blit(sortImg, (699, 169))
            self.window.blit(sortImg, (819, 169))
            self.window.blit(sortAmountDownImg, (699, 169))
            
    def shortenNameToFit(self, name):
        textSize = font.size(name)
        if textSize[0] > 334:
            while textSize[0] > 334:
                name = name[0:len(name)-1]
                textSize = font.size(name)
            name+="."
            textSize = font.size(name)
            while textSize[0] > 334:
                name = name[0:len(name)-2]
                name+="."
                textSize = font.size(name)
            name+=".."
            textSize = font.size(name)
            while textSize[0] > 334:
                name = name[0:len(name)-3]
                name+=".."
                textSize = font.size(name)
            name+="..."
            textSize = font.size(name)
            while textSize[0] > 334:
                name = name[0:len(name)-4]
                name+="..."
                textSize = font.size(name)
        return name
    
    def quitWindow(self):
        pygame.display.quit()
        quit()
    
    def drawErrorPage(self):
        Err = True
        while Err:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    Err = False
            self.window.fill(white)
            self.W.text("Error occured: Can't reach the DataBase", display_width/2, display_heigth/2)
            self.W.button(self.window, "Disagree", font, display_width/2, 455, 300, 80, btn, highlight_btn, self.quitWindow)
        self.quitWindow()
    
class Window():

    def __init__(self, displayWidth, displayHeigth, Caption, startingpage, *args):
        self.window = pygame.display.set_mode((display_width, display_heigth))
        pygame.display.set_caption(Caption)
        self.clock = pygame.time.Clock()
        self.username = ""
        if startingpage == "MainMenu" and len(args) != 0:
            self.playerID = args[0]
            self.username = self.getUsername(args[0])
        else:
            self.playerID = None
        self.Username = True
        self.Password = False
        self.verificationError = False
        self.createdAccount = 0
        self.sortByAlpha = 0
        self.sortByNumeric = 0
        self.sortByAmount = 0
        self.W = Widgets(self.window)
        #self.redrawWindow("Alert")
        self.redrawWindow(startingpage)
        
    def redrawWindow(self, pageName):
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quitWindow()
            
            if(pageName == "Alert"):
                self.drawAlert()
            elif (pageName == "Login"):
                self.drawLogin()
            elif (pageName == "LoadGame"):
                self.drawTable()
            elif (pageName == "MainMenu"):
                self.drawMenu()
            elif (pageName == "CreateAccount"):
                self.drawCreateUsername()
            elif (pageName == "ErrorPage"):
                self.drawErrorPage()
            
            pygame.display.update()
            self.clock.tick(60)
    
    def drawErrorPage(self):
        self.window.fill(white)
        self.W.text("Error occured: Couldn’t connect to the DataBase", display_width/2, display_heigth/2)
        self.W.button("Quit", font, 490, 455, 300, 80, btn, highlight_btn, self.quitWindow)
    
    def drawAlert(self):
        self.window.fill(white)
        self.W.text("WARNING: This is an Alpha program! Use at your own risk!", display_width/2, display_heigth/2)
        self.W.button("Agree", font, 150, 455, 300, 80, btn, highlight_btn, lambda: self.redrawWindow("Login"))
        self.W.button("Disagree", font, 825, 455, 300, 80, btn, highlight_btn, self.quitWindow)
    
    def drawLogin(self):
        try:
            L = Login()
            self.username = self.drawUsername()
            password = self.drawPassword()
            if L.validateLogin(self.username, password):
                self.verificationError = False
                dbAgent = dbc.DbConnector("UserLoginData")
                self.playerID = dbAgent.returnQueryList("SELECT UserID FROM Sudoku.{} WHERE Username = %s", (self.username,))
                self.redrawWindow("MainMenu")
            else:
                self.verificationError = True 
        except:
            self.redrawWindow("ErrorPage")

    def drawUsername(self):
        Input = pi.TextInput()
        while self.Username:
            self.window.fill(white)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
            if(Input.update(events) == 1):
                self.submit()
            self.window.blit(Input.get_surface(), (490, 341))

            self.W.text("Username:", 497, 300)
            if self.verificationError == True:
                self.W.text("User details not found", display_width/2, 680)
            elif self.createdAccount == 1:
                self.W.text("User created succesfully", display_width/2, 680)
            elif self.createdAccount == -1:
                self.W.text("Failed to create user", display_width/2, 680)
            self.W.button("Continue", font, 417, 510, 200, 60, btn, highlight_btn, self.submit)
            self.W.button("Cancel", font, 663, 510, 200, 60, btn, highlight_btn, self.quitWindow)
            self.W.button("Don't have an account? Create one", font_small, 417, 590, 446, 60, btn, highlight_btn, self.createAccount)
            pygame.display.update()
            self.clock.tick(60)
        return Input.get_text()
            
    def drawCreateUsername(self):
        Input = pi.TextInput()
        while self.Username:
            self.window.fill(white)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if(Input.update(events) == 1):
                self.submit()
            self.window.blit(Input.get_surface(), (490, 341))

            self.W.text("Create Username:", display_width/2, 300)
            self.W.button("Continue", font, 417, 510, 200, 60, btn, highlight_btn, self.submit)
            self.W.button("Cancel", font, 663, 510, 200, 60, btn, highlight_btn, lambda: self.redrawWindow("Login"))
            pygame.display.update()
            self.clock.tick(60)
        return Input.get_text()
    
    def drawPassword(self):
        Input = pi.TextInput()
        while self.Password:
            self.window.fill(white)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if(Input.update(events) == 1):
                self.submit()
            Input.convertToPassword()
            self.window.blit(Input.get_surface(), (490, 341))
        
            self.W.text("Password:", 497, 300)
            self.W.button("Login", font, 417, 510, 200, 60, btn, highlight_btn, self.submit)
            self.W.button("Cancel", font, 663, 510, 200, 60, btn, highlight_btn, self.quitWindow)
            pygame.display.update()
            self.clock.tick(60)
        return Input.convertToPassword()

    def drawCreatePassword(self):
        Input = pi.TextInput()
        while self.Password:
            self.window.fill(white)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if(Input.update(events) == 1):
                self.submit()
            self.window.blit(Input.get_surface(), (490, 341))
        
            self.W.text("Create Password:", display_width/2, 300)
            self.W.button("Create", font, 417, 510, 200, 60, btn, highlight_btn, self.submit)
            self.W.button("Cancel", font, 663, 510, 200, 60, btn, highlight_btn, lambda: self.redrawWindow("Login"))
            pygame.display.update()
            self.clock.tick(60)
        return Input.get_text()

    def drawTable(self):
        self.window.fill(white)
        self.W.text("Load Game", display_width/2, 115)
        self.W.small_text(self.username, 1200, 25)
        self.W.button("Log Out", font_small, 1130, 45, 140, 35, btn, highlight_btn, lambda: self.redrawWindow("Login"))
        self.W.button("Back", font_small, 15, 10, 140, 35, btn, highlight_btn, lambda: self.redrawWindow("MainMenu"))
        self.W.button("", font, 259, 164, 382, 30, btn, highlight_btn, lambda: self.sort("Alpha"))
        self.W.button("", font, 650, 164, 111, 30, btn, highlight_btn,  lambda: self.sort("Amount"))
        self.W.button("", font, 771, 164, 111, 30, btn, highlight_btn, lambda: self.sort("Numeric"))
        
        Games = self.getList()
        for i in range(len(Games)):
            Row(self.window, i, self.playerID, Games[i])
                    
    def getList(self):
        try:
            List = li(self.playerID[0][0])
            if self.sortByAlpha != 0:
                if self.sortByAlpha == 1:
                    return List.getGames("Alpha Up")
                elif self.sortByAlpha == -1:
                    return List.getGames("Alpha Down")
            elif self.sortByNumeric != 0:
                if self.sortByNumeric == 1:
                    return List.getGames("Numeric Up")
                elif self.sortByNumeric == -1:
                    return List.getGames("Numeric Down")
            elif self.sortByAmount != 0:
                if self.sortByAmount == 1:
                    return List.getGames("Amount Up")
                elif self.sortByAmount == -1:
                    return List.getGames("Amount Down")
            return List.getGames("Unsorted")
        except:
            self.redrawWindow("ErrorPage")
        
    def drawMenu(self):
        self.window.fill(white)
        self.W.text("Main Menu", display_width/2, 115)
        print("ok", self.username)
        self.W.small_text(self.username, 1200, 25)
        self.W.button("Log Out", font_small, 1130, 45, 140, 35, btn, highlight_btn, lambda: self.redrawWindow("Login"))
        self.W.button("New Game", font, 490, 202, 300, 60, btn, highlight_btn, self.startGame)
        self.W.button("Load Game", font, 490, 303, 300, 60, btn, highlight_btn, lambda: self.redrawWindow("LoadGame"))
        self.W.button("Quit", font, 490, 404, 300, 60, btn, highlight_btn, self.quitWindow)

    def startGame(self):
        pygame.display.quit()
        GUI.startgame(self.playerID)
        
    def submit(self):
        if self.Username and not self.Password:
            self.Username = False
            self.Password = True
        elif not self.Username and self.Password:
            self.Username = True
            self.Password = False

    def getUsername(self, ID):
        dbAgent = dbc.DbConnector("UserLoginData")
        username = dbAgent.returnSpecificQuery("SELECT Username FROM Sudoku.{} WHERE UserID = %s", (ID,))
        return username

    def sort(self, sortBy):
        thisturn = False
        if sortBy == "Alpha":
            if self.sortByAlpha == 0 or self.sortByAlpha == -1:
                self.sortByAlpha = 1
                thisturn = True
            if not thisturn and self.sortByAlpha == 1:
                self.sortByAlpha = -1
            self.sortByNumeric = 0
            self.sortByAmount = 0           
        elif sortBy == "Amount":
            if self.sortByAmount == 0 or self.sortByAmount == -1:
                self.sortByAmount = 1
                thisturn = True
            if not thisturn and self.sortByAmount == 1:
                self.sortByAmount = -1
            self.sortByAlpha = 0
            self.sortByNumeric = 0
        elif sortBy == "Numeric":
            if self.sortByNumeric == 0 or self.sortByNumeric == -1:
                self.sortByNumeric = 1
                thisturn = True
            if not thisturn and self.sortByNumeric == 1:
                self.sortByNumeric = -1
            self.sortByAlpha = 0
            self.sortByAmount = 0
        
    def createAccount(self):
        try:
            dbAgent = dbc.DbConnector("UserLoginData")
            L = Login()
            create_username = self.drawCreateUsername()
            create_password = self.drawCreatePassword()
            dbAgent.insertQuery((create_username, create_password))
            if L.validateLogin(create_username, create_password):
                self.createdAccount = 1
                self.redrawWindow("Login")
            else:
                self.createdAccount = -1
                self.redrawWindow("CreateAccount")
        except:
            self.redrawWindow("ErrorPage")
    
    def quitWindow(self):
        pygame.display.quit()
        quit()


if __name__ == "__main__":
    win = Window(display_width, display_heigth, "Sudoku", "Login")
    pygame.quit()
    quit()