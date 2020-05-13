import mysql.connector as mysql
import json

class DbConnector():
    def __init__(self, title):
        self.credentials = self.getCredentials()
        self.connection = self.makeConnection()
        self.tableTitle = title
        self.QueryDictionary = {
            "Insert" : "INSERT INTO {} (Username, Passwd) VALUES (%s, %s)".format(self.tableTitle),
            "ReturnAll" : "SELECT * FROM {}".format(self.tableTitle),
            "Delete" : "DELETE FROM {} WHERE UserID = %s".format(self.tableTitle),
        }
    
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

    def runQuery(self, query, args):
        cursor = self.connection.cursor()
        cursor.execute(query, args)
        self.connection.commit()
        
    def returnQueryList(self, query):
        cursor = self.connection.cursor()
        result = cursor.execute(query)
        resultList = cursor.fetchall()
        return resultList


#Create Login object
Login = DbConnector("UserLoginData")

# Inserts a  created user
# User = ("Player 1", "password")
# Login.runQuery(Login.QueryDictionary["Insert"], User)

#Deletes a user by key
UserID = (11,)
Login.runQuery(Login.QueryDictionary["Delete"], UserID)

#Print all rows in UserLoginData 
result = Login.returnQueryList(Login.QueryDictionary["ReturnAll"])

for row in result:  
    print(row)

Login.connection.close()
