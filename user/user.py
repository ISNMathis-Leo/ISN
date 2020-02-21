import hashlib

from maintest import Main


class User:
    def __init__(self, id, name, nickname, encrypted_password, email, notes, abrevs, categories):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.encrypted_password = encrypted_password
        self.email = email
        self.notes = notes
        self.abrevs = abrevs
        self.categories = categories

    @classmethod
    def getUser(cls, identifier):
        sql = "SELECT * FROM notepad WHERE nickname = %s OR email = %s"
        val = (identifier, identifier,)
        Main.db.cursor.execute(sql, val)
        result = Main.db.cursor.fetchall()

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

    @classmethod
    def userLogin(cls, identifier, password):
        encrypted_password = hashlib.sha256(password.encode())
        sql = "SELECT * FROM notepad WHERE (nickname = %s OR email = %s) AND encrypted_password = %s"
        val = (identifier, identifier, encrypted_password.hexdigest(),)
        Main.db.cursor.execute(sql, val)
        result = Main.db.cursor.fetchone()

        if result:
            print("Logged in !")
            return cls.getUser(identifier)
        else:
            print("Incorrect username/password!")

    @classmethod
    def userCreate(cls, name, username, password, email):

        sql = "SELECT nickname, email FROM notepad WHERE nickname= %s OR email = %s"
        val = (username, email)
        Main.db.execute(sql, val)
        result = Main.db.cursor.fetchone()

        if result:
            print("Username or Email already used !")
        else:
            encrypted_password = hashlib.sha256(password.encode())
            sql = "INSERT INTO `notepad`(`name`, `nickname`, `encrypted_password`, `email`, `notes`, `abrevs`, " \
                  "`categories`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (name, username, encrypted_password.hexdigest(), email, "", "", "")
            Main.db.cursor.execute(sql, val)
            Main.db.db.commit()
