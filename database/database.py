import mysql.connector
from user.user import User


class Database:

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = mysql.connector.connect(
            host="remotemysql.com",
            user="9Nxz1gWfXK",
            passwd="7zrnREDcJr",
            database="9Nxz1gWfXK"
        )

        self.cursor = self.db.cursor()

    def createNewUser(self, name, nickname, encrypted_password, email, notes, abrevs, categories):
        sql = "INSERT INTO notepad (name, nickname, encrypted_password, email, notes, abrevs, categories) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, nickname, encrypted_password, email, notes, abrevs, categories)
        self.cursor.execute(sql, val)
        self.db.commit()
        print("done")

    def getUser(self, identifier):
        sql = "SELECT * FROM notepad WHERE nickname = %s OR email = %s"
        val = (identifier, identifier, )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        for x in result:
            id = x[0]
            name = x[1]
            nickname = x[2]
            ep = x[3]
            email = x[4]
            notes = x[5]
            abrevs = x[6]
            cat = x[7]

        return User(id, name, nickname, ep, email, notes, abrevs, cat)
