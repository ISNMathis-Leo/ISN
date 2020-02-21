import hashlib
import json
from user.note import Note


class User:
    db = None

    def __init__(self, id, name, username, password, email):

        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def setDatabase(cls, database):
        global db
        db = database

    @classmethod
    def getUser(cls, identifier):
        sql = "SELECT * FROM users WHERE nickname = %s OR email = %s OR id = %s"
        val = (identifier, identifier, identifier)
        db.cursor.execute(sql, val)
        result = db.cursor.fetchall()

        for x in result:
            id = x[0]
            name = x[1]
            nickname = x[2]
            ep = x[3]
            email = x[4]

        return User(id, name, nickname, ep, email)

    @classmethod
    def login(cls, identifier, password):
        encrypted_password = hashlib.sha256(password.encode())
        sql = "SELECT * FROM users WHERE (nickname = %s OR email = %s) AND encrypted_password = %s"
        val = (identifier, identifier, encrypted_password.hexdigest(),)
        db.cursor.execute(sql, val)
        result = db.cursor.fetchone()

        if result:
            print("Logged in !")
            return cls.getUser(identifier)
        else:
            print("Incorrect username/password!")

    def createAccountAndPush(self):
        sql = "SELECT nickname, email FROM users WHERE nickname= %s OR email = %s"
        val = (self.username, self.email)
        db.cursor.execute(sql, val)
        result = db.cursor.fetchone()

        if result:
            print("Username or Email already used !")
        else:
            encrypted_password = hashlib.sha256(self.password.encode())
            sql = "INSERT INTO `users`(`name`, `nickname`, `encrypted_password`, `email`  VALUES (%s,%s,%s,%s)"
            val = (self.name, self.username, encrypted_password.hexdigest(), self.email)
            db.cursor.execute(sql, val)
            db.db.commit()

    def loadNotes(self):
        global notes
        sql = "SELECT notes FROM notes WHERE account_id= %s"
        val = (self.id,)
        db.cursor.execute(sql, val)
        result = db.cursor.fetchone()

        if result is None:
            return []
        else:
            json_dict = json.loads(result[0])

            notes = []
            for i in range(0, len(json_dict["notes"])):
                notes.append(
                    Note(json_dict["notes"][i]["id"], json_dict["notes"][i]["title"], json_dict["notes"][i]["category"],
                         json_dict["notes"][i]["creation_date"], json_dict["notes"][i]["last_edit_date"],
                         json_dict["notes"][i]["content"]))

            return notes

    def createNoteAndPush(self, id, title, category_id, current_date, content):

        sql = "SELECT notes FROM notes WHERE account_id= %s"
        val = (self.id,)
        db.cursor.execute(sql, val)
        result = db.cursor.fetchone()

        if result is None:

            data = {"notes": [{"id": id, "title": title, "category": category_id, "creation_date": current_date,
                               "last_edit_date": current_date, "content": content}]}
            data_dump = json.dumps(data)

            sql = "INSERT INTO `notes`(`account_id`, `notes`) VALUES (%s, %s)"
            val = (self.id, data_dump,)

            db.cursor.execute(sql, val)
            db.db.commit()

        else:

            data = {"id": id, "title": title, "category": category_id, "creation_date": current_date,
                    "last_edit_date": current_date, "content": content}

            json_dict = json.loads(result[0])
            json_dict["notes"].append(data)

            json_dump = json.dumps(json_dict)


            print(json_dump)

            sql = "UPDATE notes SET notes = %s WHERE account_id = %s"
            val = (json_dump, self.id)

            db.cursor.execute(sql, val)
            db.db.commit()