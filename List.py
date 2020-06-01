import pygame
import db_connector as dbc
import json

class ListItem():
    def __init__(self, ID):
        self.dbAgent = dbc.DbConnector("Sudoku")
        self.UserID = ID
        
        
    def getGames(self, sortMethod):
        mainQuery = """
                    SELECT
                    Sudoku.SudokuName, Sudoku.TimeCurrent, Sudoku.CellsLeft, UserLoginData.Username, Sudoku.SudokuID, Sudoku.Board
                    FROM UserData
                    INNER JOIN Sudoku ON UserData.SudokuID = Sudoku.SudokuID
                    INNER JOIN UserLoginData ON UserData.UserID = UserLoginData.UserID
                    WHERE UserLoginData.UserID = %s
                    """
        if sortMethod == "Unsorted":
            result = self.dbAgent.returnQueryList(mainQuery, (self.UserID,))
        elif sortMethod == "Alpha Up":
            result = self.dbAgent.returnQueryList((mainQuery + " ORDER BY Sudoku.SudokuName ASC"), (self.UserID,))
        elif sortMethod == "Alpha Down":
            result = self.dbAgent.returnQueryList((mainQuery + " ORDER BY Sudoku.SudokuName DESC"), (self.UserID,))
        elif sortMethod == "Numeric Up":
            result = self.dbAgent.returnQueryList((mainQuery + " ORDER BY Sudoku.TimeCurrent DESC"), (self.UserID,))
        elif sortMethod == "Numeric Down":
            result = self.dbAgent.returnQueryList((mainQuery + " ORDER BY Sudoku.TimeCurrent ASC"), (self.UserID,))
        elif sortMethod == "Amount Up":
            result = self.dbAgent.returnQueryList((mainQuery + " ORDER BY Sudoku.CellsLeft ASC"), (self.UserID,))
        elif sortMethod == "Amount Down":
            result = self.dbAgent.returnQueryList((mainQuery + " ORDER BY Sudoku.CellsLeft DESC"), (self.UserID,))
        return result

if __name__ == "__main__":
    li = ListItem(1)
    games = li.getGames("Unsorted")
    t = json.loads(games[0][5])
    print(type(t))