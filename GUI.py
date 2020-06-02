import threading
import generator
import pygame
import time
import db_connector as dbc
import pyGUI
import pygameInput as pi
import json

#Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (186, 18 ,0)
delete_red = (241, 157, 157)
play_green = (160, 241, 157)
btn = (157, 209, 241)
highlight_btn = (200, 224, 244)

#Fonts
pygame.font.init()
font = pygame.font.SysFont("comicsans", 40)
font_small = pygame.font.SysFont("comicsans", 24)
font_40 = pygame.font.SysFont("robotoregularttf", 40)
font_32 = pygame.font.SysFont("robotoregularttf", 32)
font_24 = pygame.font.SysFont("robotoregularttf", 24)
font_20 = pygame.font.SysFont("robotoregularttf", 20)

class Grid:
    sudoku = generator.Sudoku(9, 43)#43
    board = sudoku.returnBoard()

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win


    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def text_objects(text, font, color):
    pygame.font.init()
    textSurface = font.render(text, 1, color)
    return textSurface, textSurface.get_rect()

def text(win, text, font, x, y):
    pygame.font.init()
    TextSurf, TextRect = text_objects(text, font, black)
    TextRect.center = ((x), (y))
    win.blit(TextSurf, TextRect)

def button(window, msg, font, x,y,w,h,ic,ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
            time.sleep(0.15)
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))
    textSurf, textRect = text_objects(msg, font, black)
    textRect.center = ( (x+(w/2), y+(h/2)) )
    window.blit(textSurf, textRect)

def loadMenu(playerID):
    pygame.display.quit()
    pyGUI.Window(1280, 720, "Sudoku", "MainMenu", playerID)
    
def quitProgram():
    pygame.display.quit()
    quit()
    
def postSave(win, exception, *args):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 40)
    font_small = pygame.font.SysFont("comicsans", 24)
    font_40 = pygame.font.SysFont("robotoregularttf", 40)
    font_32 = pygame.font.SysFont("robotoregularttf", 32)
    font_24 = pygame.font.SysFont("robotoregularttf", 24)
    font_20 = pygame.font.SysFont("robotoregularttf", 20)
    excep=True
    while excep:
        win.fill(white)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                excep = False
        
        text(win, exception, font_32, 270, 263)
        if exception != "Error occured: Couldn't save to DB":
            button(win, "Back to Main Menu", font_20, 173, 327, 195, 30, btn, highlight_btn, lambda: loadMenu(args[0]))
        button(win, "Quit", font_20, 173, 364, 195, 30, btn, highlight_btn, quitProgram)
        
        pygame.display.update()
    quitProgram()
    
def rewrite(win, name, timeCompleted, currentTime, cellsLeft, done, table, *args):
    if len(args) != 1:
        uName = args[2]
    else:
        uName=name

    dbAgent = dbc.DbConnector("Sudoku")
    dbAgent.rewriteSudoku((timeCompleted, currentTime, cellsLeft, done, table, uName))
    postSave(win, "Succesfully saved!", args[0])
    # except:
    #     postSave(win, "Error occured: Couldn't save to DB")
    
def upload(win, name, timeCompleted, currentTime, cellsLeft, done, table, playerID, *args):
    if len(args) != 1:
        uName = args[2]
    else:
        uName=name
    try:        
        dbAgent = dbc.DbConnector("Sudoku")
        dbAgent.saveSudoku((uName, timeCompleted, currentTime, cellsLeft, done, table))
        result = dbAgent.returnQueryList("SELECT SudokuID FROM Sudoku.{} WHERE SudokuName = %s", (uName,))
        sudokuID = result[0][0]
        dbAgent.connectSudokuPlayer((playerID, sudokuID))
        postSave(win, "Succesfully saved!", playerID)
    except:
        postSave(win, "Error occured: Couldn't save to DB")
    
def countEmptyCells(bo):
    empty = 0
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j].value == 0:
                empty+=1
    return empty

def parseToString(bo):
    stringTable ="["
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if j == 0:
                stringTable+='['
            stringTable+=str(bo[i][j].value)
            if j != 8:
                stringTable+=", "
            if j == 8 and i != 8:
                stringTable+= "], "
            elif j == 8 and i == 8:
                stringTable+="]]"
    return stringTable

def getName(name):
    dbAgent = dbc.DbConnector("Sudoku")
    result = dbAgent.returnQueryList("SELECT * FROM Sudoku.{} WHERE SudokuName = %s", (name,))
    if len(result) != 0:
        return True
    return False

def saveNquit(win, currentTable, start, *args):
    if len(args) == 1:
        try:
            playerID = args[0][0][0]
        except:
            playerID = args[0]
        currentTime = format_time(round(time.time()-start))
    else:
        playerID = args[0]
        currentTime = format_time(round(time.time()-start), args[5])
    cellsLeft = countEmptyCells(currentTable)
    table = parseToString(currentTable)
    if cellsLeft == 0:
        done = True
        timeCompleted = currentTime
    else:
        done = False
        timeCompleted = None
        
    print("Id: ", playerID, "Curent time:", currentTime, "Completed time:", timeCompleted, "Cells left:", cellsLeft, "Done:", done, "Table:", table)
    clock = pygame.time.Clock()
    
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 40)
    font_small = pygame.font.SysFont("comicsans", 24)
    font_40 = pygame.font.SysFont("robotoregularttf", 40)
    font_32 = pygame.font.SysFont("robotoregularttf", 32)
    font_24 = pygame.font.SysFont("robotoregularttf", 24)
    font_20 = pygame.font.SysFont("robotoregularttf", 20)
    if len(args) != 1:
        Input = pi.TextInput(initial_string=args[2], font_size=24)
    else:
        Input = pi.TextInput(font_size=24)
    save=True
    while save:
        win.fill(white)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                save = False
        Input.update(events)
        name = Input.get_text()
        win.blit(Input.get_surface(), (225, 201))
        
        text(win, "Save & Quit", font_32, (540 - 540/2), 84)
        
        text(win, "Name:", font_24, 186, 215)
        button(win,"", font, 222, 230, 277, 1, black, black)#acts like a line
        
        text(win, "Time:", font_24, 191, 250)
        text(win, currentTime, font_24, 247, 250)
        button(win,"", font, 222, 265, 277, 1, black, black)#acts like a line
        
        text(win, "Empty cells left:", font_24, 135, 285)
        if cellsLeft <= 9:
            text(win, str(cellsLeft), font_24, 232, 285)
        else:
            text(win, str(cellsLeft), font_24, 238, 285)
        button(win,"", font, 222, 300, 277, 1, black, black)#acts like a line
        
        text(win, "Cells completed:", font_24, 130, 320)
        cellsCompleted = 81 - cellsLeft
        text(win, (str(cellsCompleted)+"/81"), font_24, 254, 320)
        button(win,"", font, 222, 335, 277, 1, black, black)#acts like a line
        
        text(win, "Completed:", font_24, 157, 355)
        if done:
            text(win, "Yes", font_24, 244, 355)
        else:
            text(win, "No", font_24, 241, 355)
        button(win,"", font, 222, 370, 277, 1, black, black)#acts like a line
        
        if getName(name):
            button(win, "Rewrite", font_20, 195, 449, 150, 30, btn, highlight_btn, lambda: rewrite(win, name, timeCompleted, currentTime, cellsLeft, done, table, *args))
        button(win, "Save", font_20, 195, 484, 150, 30, btn, highlight_btn, lambda: upload(win, name, timeCompleted, currentTime, cellsLeft, done, table, playerID, *args))
        button(win, "Cancel", font_20, 195, 519, 150, 30, btn, highlight_btn, quitProgram)
        
        pygame.display.update()
    
def redraw_window(win, board, currentTable, time, strikes, start, *args):
    #Fonts
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 40)
    font_small = pygame.font.SysFont("comicsans", 24)
    font_40 = pygame.font.SysFont("robotoregularttf", 40)
    font_32 = pygame.font.SysFont("robotoregularttf", 32)
    font_24 = pygame.font.SysFont("robotoregularttf", 24)
    font_20 = pygame.font.SysFont("robotoregularttf", 20)
    win.fill(white)
    # Draw time
    if len(args) != 1:
        txt = font.render("Time: " + format_time(time, args[5]), 1, black)
    else:
        txt = font.render("Time: " + format_time(time), 1, black)
    win.blit(txt, (540 - 160, 560))
    # Draw Strikes
    txt = font.render((str(strikes) + "X"), 1, red)
    if strikes != 0:
        win.blit(txt, (20, 560))
    # Draw grid and board
    board.draw()
    # Draw butons
    button(win, "Save & Quit", font_small, 270,550,100,40,btn,highlight_btn, lambda: saveNquit(win, currentTable, start, *args))
    solve = threading.Thread(target=board.solve_gui)
    button(win, "Solve", font_small, 150,550,100,40,btn,highlight_btn, solve.start)

def format_time(secs, *args):
    if args:
        secs=secs+args[0]
        sec = secs%60
    else:
        sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat
    
def main(start, *args):
    print("main:", args)
    pygame.init()
    win = pygame.display.set_mode((540,600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    strikes = 0
    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_s:
                    solve = threading.Thread(target=board.solve_gui)
                    solve.start()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                        elif(strikes>5):
                            print("Game over")
                            run = False
                            pygame.display.quit()
                            return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)
        currentTable = board.cubes
        redraw_window(win, board, currentTable, play_time, strikes, start, *args)
        clock.tick(60)
        pygame.display.update()
        
    return play_time

def loadGame(*args):
    print("load:", args)
    pygame.init()
    win = pygame.display.set_mode((540,600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    table = json.loads(args[4])
    print("table:", table, type(table))
    board.cubes = [[Cube(table[i][j], i, j, 540, 540) for j in range(9)] for i in range(9)]
    key = None
    run = True
    strikes = 0
    divisorIndex = str(args[3]).find(':')
    startSeconds = int(float(args[3][0:divisorIndex]))*60 + int(float(args[3][divisorIndex+1:]))
    args += startSeconds,
    print("load-appended:", args)
    start = time.time()
    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_s:
                    solve = threading.Thread(target=board.solve_gui)
                    solve.start()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                        elif(strikes>5):
                            print("Game over")
                            run = False
                            pygame.display.quit()
                            return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)
        currentTable = board.cubes
        redraw_window(win, board, currentTable, play_time, strikes, start, *args)
        clock.tick(60)
        pygame.display.update()
        
    return play_time

def startgame(playerID):
    start = time.time()
    main(start, playerID)

if __name__ == "__main__":
    pyGUI.Window(1280, 720, "Sudoku", "Login")
    pygame.quit()
    quit()