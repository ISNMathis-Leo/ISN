from database.database import Database
from user.user import User


class Main:

    db = Database()
    db.connect()

    User.setDatabase(db)

    user = User.login("cc", "cc2")

    # User.userCreate("Adam Cavillon", "dandan2611", "salutlesbogos", "dindon@gmail.com")
