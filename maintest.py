from database.database import Database
from user.user import User


class Main:
    db = Database()
    db.connect()
    # db.createNewUser("michel", "bonjour", "cc", "cc", "cc", "cc", "cc")

    user = db.getUser("bonjour")

    print(user.name)
    print(user.nickname)
