from database.database import Database
from user.user import User


class Main:
    db = Database()
    db.connect()

    id = input("Nom d'utilisateur ou email : ")
    pswd = input("Mot de passe : ")
    user = db.userLogin(id, pswd)

    print(user.name)
    print(user.nickname)
