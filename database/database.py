import mysql.connector


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
