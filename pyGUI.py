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
play_green = (160, 241, 157)
btn = (157, 209, 241)
highlight_btn = (200, 224, 244)

#Fonts
font = pygame.font.SysFont("robotoregularttf", 40)
font_small = pygame.font.SysFont("robotoregularttf", 24)

class Window():

    def __init__(self, displayWidth, displayHeigth, Caption):
        self.window = pygame.display.set_mode((display_width, display_heigth))
        pygame.display.set_caption(Caption)
        self.clock = pygame.time.Clock()
        self.playerID = None
        self.Username = True
        self.Password = False
        self.username = ""
        self.verificationError = False
        self.createdAccount = 0
        #self.redrawWindow("Alert")
        self.redrawWindow("Login")
        
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
            
            pygame.display.update()
            self.clock.tick(60)
    
    def drawAlert(self):
        self.window.fill(white)
        self.text("WARNING: This is an Alpha program! Use at your own risk!", display_width/2, display_heigth/2)
        self.button(self.window, "Agree", font, 150, 455, 300, 80, btn, highlight_btn, lambda: self.redrawWindow("Login"))
        self.button(self.window, "Disagree", font, 825, 455, 300, 80, btn, highlight_btn, self.quitWindow)
    
    def drawLogin(self):
        L = Login()
        self.username = self.drawUsername()
        password = self.drawPassword()
        if L.validateLogin(self.username, password):
            self.verificationError = False
            dbAgent = dbc.DbConnector("UserLoginData")
            self.playerID = dbAgent.returnQueryList("SELECT UserID FROM Sudoku.{} WHERE Username = %s", (self.username,))
            print(self.playerID)
            self.redrawWindow("MainMenu")
        else:
            self.verificationError = True 

    def drawUsername(self):
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

            self.text("Username:", 497, 300)
            if self.verificationError == True:
                self.text("User details not found", display_width/2, 680)
            elif self.createdAccount == 1:
                self.text("User created succesfully", display_width/2, 680)
            elif self.createdAccount == -1:
                self.text("Failed to create user", display_width/2, 680)
            self.button(self.window, "Continue", font, 417, 510, 200, 60, btn, highlight_btn, self.submit)
            self.button(self.window, "Cancel", font, 663, 510, 200, 60, btn, highlight_btn, self.quitWindow)
            self.button(self.window, "Don't have an account? Create one", font_small, 417, 590, 446, 60, btn, highlight_btn, self.createAccount)
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

            self.text("Create Username:", display_width/2, 300)
            self.button(self.window, "Continue", font, 417, 510, 200, 60, btn, highlight_btn, self.submit)
            self.button(self.window, "Cancel", font, 663, 510, 200, 60, btn, highlight_btn, lambda: self.redrawWindow("Login"))
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
        
            self.text("Password:", 497, 300)
            self.button(self.window, "Login", font, 417, 510, 200, 60, btn, highlight_btn, self.submit)
            self.button(self.window, "Cancel", font, 663, 510, 200, 60, btn, highlight_btn, self.quitWindow)
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
        
            self.text("Create Password:", display_width/2, 300)
            self.button(self.window, "Create", font, 417, 510, 200, 60, btn, highlight_btn, self.submit)
            self.button(self.window, "Cancel", font, 663, 510, 200, 60, btn, highlight_btn, lambda: self.redrawWindow("Login"))
            pygame.display.update()
            self.clock.tick(60)
        return Input.get_text()

    def drawTable(self):
        self.window.fill(white)
        self.text("Load Game", display_width/2, 115)
        self.small_text(self.username, 1200, 25)
        self.button(self.window, "Log Out", font_small, 1130, 45, 140, 35, btn, highlight_btn, lambda: self.redrawWindow("Login"))
        

    def drawMenu(self):
        self.window.fill(white)
        self.text("Main Menu", display_width/2, 115)
        self.small_text(self.username, 1200, 25)
        self.button(self.window, "Log Out", font_small, 1130, 45, 140, 35, btn, highlight_btn, lambda: self.redrawWindow("Login"))
        self.button(self.window, "New Game", font, 490, 202, 300, 60, btn, highlight_btn, self.startGame)
        self.button(self.window, "Load Game", font, 490, 303, 300, 60, btn, highlight_btn, lambda: self.redrawWindow("LoadGame"))
        self.button(self.window, "Quit", font, 490, 404, 300, 60, btn, highlight_btn, self.quitWindow)
    
    
    #Widgets
    def startGame(self):
        pygame.quit()
        GUI.startgame(self.playerID)
        
    def submit(self):
        if self.Username and not self.Password:
            self.Username = False
            self.Password = True
        elif not self.Username and self.Password:
            self.Username = True
            self.Password = False
    
    def createAccount(self):
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
    
    def text(self, text, x, y):
        TextSurf, TextRect = self.text_objects(text, font, black)
        TextRect.center = ((x), (y))
        self.window.blit(TextSurf, TextRect)
    
    def small_text(self, text, x, y):
        TextSurf, TextRect = self.text_objects(text, font_small, black)
        TextRect.center = ((x), (y))
        self.window.blit(TextSurf, TextRect)
        
    def text_objects(self, text, font, color):
        textSurface = font.render(text, 1, color)
        return textSurface, textSurface.get_rect()

    def button(self, window, msg, font, x,y,w,h,ic,ac, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(window, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
                time.sleep(0.15)
        else:
            pygame.draw.rect(window, ic, (x, y, w, h))
        textSurf, textRect = self.text_objects(msg, font, black)
        textRect.center = ( (x+(w/2), y+(h/2)) )
        window.blit(textSurf, textRect)

    def quitWindow(self):
        pygame.quit()
        quit()

if __name__ == "__main__":
    Window(display_width, display_heigth, "Sudoku")
    pygame.quit()
    quit()