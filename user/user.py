import hashlib


class User:
    db = None

    def __init__(self, id, name, username, password, email, notes, abrevs, categories):

        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.notes = notes
        self.abrevs = abrevs
        self.categories = categories

    @classmethod
    def setDatabase(cls, database):
        global db
        db = database

    @classmethod
    def getUser(cls, identifier):
        sql = "SELECT * FROM notepad WHERE nickname = %s OR email = %s OR id = %s"
        val = (identifier, identifier, identifier)
        db.cursor.execute(sql, val)
        result = db.cursor.fetchall()

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
    def login(cls, identifier, password):
        encrypted_password = hashlib.sha256(password.encode())
        sql = "SELECT * FROM notepad WHERE (nickname = %s OR email = %s) AND encrypted_password = %s"
        val = (identifier, identifier, encrypted_password.hexdigest(),)
        db.cursor.execute(sql, val)
        result = db.cursor.fetchone()

        if result:
            print("Logged in !")
            return cls.getUser(identifier)
        else:
            print("Incorrect username/password!")

    def createAndPush(self):
        sql = "SELECT nickname, email FROM notepad WHERE nickname= %s OR email = %s"
        val = (self.username, self.email)
        db.cursor.execute(sql, val)
        result = db.cursor.fetchone()

        if result:
            print("Username or Email already used !")
        else:
            encrypted_password = hashlib.sha256(self.password.encode())
            sql = "INSERT INTO `notepad`(`name`, `nickname`, `encrypted_password`, `email`, `notes`, `abrevs`, " \
                  "`categories`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            val = (self.name, self.username, encrypted_password.hexdigest(), self.email, "", "", "")
            db.cursor.execute(sql, val)
            db.db.commit()
