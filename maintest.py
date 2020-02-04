from database.database import Database
from user.user import *


def login(db):
    global user
    id = input("Nom d'utilisateur ou email : ")
    pswd = input("Mot de passe : ")
    user = db.userLogin(id, pswd)


class Main:
    db = Database()
    user = None

    db.connect()
    login(db)
