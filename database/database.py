import mysql.connector
import hashlib
from user.user import User


class Database:

    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = mysql.connector.connect(
            host="91.121.157.83",
            user="arkcos",
            passwd="qBTzPqI5xWXPyyIX",
            database="arkcos"
        )
        self.cursor = self.db.cursor()

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

    def userLogin(self, identifier, password):
        encrypted_password = hashlib.sha256(password.encode())
        sql = "SELECT * FROM notepad WHERE (nickname = %s OR email = %s) AND encrypted_password = %s"
        val = (identifier, identifier, encrypted_password.hexdigest(), )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchone()

        if result:
            print("Logged in !")
            return self.getUser(identifier)
        else:
            print("Incorrect username/password!")

    def userCreate(self, name, username, password, email):
        encrypted_password = hashlib.sha256(password.encode())
        sql = "INSERT INTO `notepad`(`name`, `nickname`, `encrypted_password`, `email`, `notes`, `abrevs`, " \
              "`categories`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (name, username, encrypted_password.hexdigest(), email, "", "", "")
        self.cursor.execute(sql, val)
        self.db.commit()


