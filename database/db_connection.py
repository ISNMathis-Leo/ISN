import mysql.connector

class DBConnection :

    def __init__(self):

        self.mydb = mysql.connector.connect(
          host="remotemysql.com",
          user="9Nxz1gWfXK",
          passwd="7zrnREDcJr",
          database="9Nxz1gWfXK"
        )

        self.cursor= self.mydb.cursor()

