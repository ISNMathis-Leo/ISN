from database.database import Database


class Main:
    db = Database()
    db.connect()
    db.createNewUser("cc", "cc", "cc", "cc", "cc", "cc", "cc")
