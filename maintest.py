from database.database import Database
from user.user import User


class Main:
    db = Database()
    db.connect()
    User.userCreate("LABADIE Pierre", "Sesax", "HELLO", "pierre@gmail.com")