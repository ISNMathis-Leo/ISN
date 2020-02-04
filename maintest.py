from database.database import Database
from user.user import *


class Main:
    db = Database()
    user = None

    db.connect()
    