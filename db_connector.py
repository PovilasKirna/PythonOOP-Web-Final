import mysql.connector as mysql
import json

class DbConnector():
    def __init__(self, title):
        self.credentials = self.getCredentials()
        self.connection = self.makeConnection()
        self.tableTitle = title
    
    def getCredentials(self):
        self.credentials = None
        with open('secrets.json') as f:
            self.credentials = json.load(f)
        return self.credentials
    
    def makeConnection(self): 
        # Ensure your credentials were setup
        if self.credentials:
            # Connect to the DB
            self.connection = mysql.connect(
                host = self.credentials.get('host'),
                user = self.credentials.get('username'),
                password = self.credentials.get('passwd'),
                database = self.credentials.get('database')
            )
        return self.connection

    def insertQuery(self, *args):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO {} (Username, Passwd) VALUES (%s, %s)".format(self.tableTitle), *args)
        self.connection.commit()
            
        
    def returnQueryList(self, query, *args):
        cursor = self.connection.cursor()
        result = cursor.execute(query.format(self.tableTitle), *args)
        resultList = cursor.fetchall()
        return resultList
    
    def printList(self, resultList):
        for row in resultList:  
            print(row)
    
    def deleteQuery(self, *args):
        cursor = self.connection.cursor()
        result = cursor.execute("DELETE FROM {} WHERE UserID = %s".format(self.tableTitle), *args)
        self.connection.commit()

    def deleteSudokuGame(self, *args):
        cursor = self.connection.cursor()
        result = cursor.execute("DELETE FROM Sudoku.{} WHERE (SudokuID = %s)".format(self.tableTitle), *args)
        self.connection.commit()

    def saveSudoku(self, *args):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Sudoku.{} (SudokuName, TimeCompleted, TimeCurrent, CellsLeft, Done, Board) VALUES (%s, %s, %s, %s, %s, %s)".format(self.tableTitle), *args)
        self.connection.commit()
    
    def connectSudokuPlayer(self, *args):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Sudoku.UserData (UserID, SudokuID) VALUES (%s, %s)", *args)
        self.connection.commit()
        
if __name__ == "__main__":
    #Create Login object
    Login = DbConnector("UserLoginData")

    #Inserts a created user
    # User = ("Player 2", "password")
    # Login.insertQuery(User)

    #Deletes user by his ID
    # UserID = (12,)
    # Login.deleteQuery(UserID)

    #Print all rows in UserLoginData 
    result = Login.returnQueryList("SELECT UserID FROM {}")
    Login.printList(result)

    Login.connection.close()