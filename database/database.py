import mysql.connector
from mysql.connector import errorcode
from files.logs import Log


class Database:

    def __init__(self):
        self.db = None
        self.cursor = None
        self.connected = False

    def connect(self):

        try:

            self.db = mysql.connector.connect(
                host="91.121.157.83",
                user="arkcos",
                passwd="qBTzPqI5xWXPyyIX",
                database="arkcos"
            )

            self.cursor = self.db.cursor()
            self.connected = True
            Log.info("Database linked !")

        except mysql.connector.Error as err:

            self.connected = False

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                Log.error("DB : Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                Log.error("DB : Database does not exist")
            else:
                print(err)
                Log.error("DB : " + str(err))





