import mysql.connector


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




