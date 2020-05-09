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

    def runQuery(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        
    def returnQueryList(self, query):
        cursor = self.connection.cursor()
        result = cursor.execute(query)
        resultList = cursor.fetchall()
        return resultList

Login = DbConnector("UserLoginData")
#Login.runQuery("CREATE TABLE UserLog (UserID int NOT NULL AUTO_INCREMENT,Username varchar(255) NOT NULL,Passwd varchar(255),PRIMARY KEY (UserID));")

LoginInsertQuery = "INSERT INTO UserLoginData (Username, Passwd) VALUES (%s, %s)"

result = Login.returnQueryList("SELECT * FROM UserLoginData")
for row in result:
    print(row)
Login.connection.close()




# cursor = connection.cursor()
# cursor.execute("SELECT * FROM UserLoginData")

# # Loop through the results
# for id, Username, Password in cursor:
#     print(f'Id: {id}, Username: {Username}, Password: {Password}')

# # Close the connection