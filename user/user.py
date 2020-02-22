import hashlib
import json
import os
import random

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

        if db.connected is True:

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

        else:
            return User(0, "offlineAccount", "offline", "offline", "offline")

    @classmethod
    def login(cls, identifier, password):

        if db.connected is True:

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

        else:
            return cls.getUser(identifier)

    def createAccountAndPush(self):

        if db.connected is True:

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

        env = os.getenv('APPDATA')

        if db.connected is True:

            notes = []

            sql = "SELECT notes FROM notes WHERE account_id= %s"
            val = (self.id,)
            db.cursor.execute(sql, val)
            result = db.cursor.fetchone()

            if result is None:
                return []
            else:
                json_dict = json.loads(result[0])

                for i in range(0, len(json_dict["notes"])):
                    notes.append(
                        Note(json_dict["notes"][i]["id"], json_dict["notes"][i]["title"],
                             json_dict["notes"][i]["category"],
                             json_dict["notes"][i]["creation_date"], json_dict["notes"][i]["last_edit_date"],
                             json_dict["notes"][i]["content"]))

                return notes

        else:

            files = []
            notes = []

            for file in os.listdir(env + "\\Notepad\\Cache\\Offline"):
                if file.startswith("offline_"):
                    files.append("Offline\\" + os.path.basename(file))

            for file in os.listdir(env + "\\Notepad\\Cache"):
                if file.endswith(".json"):
                    files.append(os.path.basename(file))

            for i in range(0, len(files)-1):
                with open(env + "\\Notepad\\Cache\\" + files[i], 'r') as content_file:
                    content = content_file.read()
                    # print("allo   " + content)
                    json_dict = json.loads(content)
                    notes.append(
                        Note(json_dict["id"], json_dict["title"], json_dict["category"], json_dict["creation_date"],
                             json_dict["last_edit_date"], json_dict["content"]))

            return notes

    def downloadNotes(self):

        env = os.getenv('APPDATA')

        if db.connected is True:

            sql = "SELECT notes FROM notes WHERE account_id= %s"
            val = (self.id,)
            db.cursor.execute(sql, val)
            result = db.cursor.fetchone()

            if result is None:
                return
            else:

                json_dict = json.loads(result[0])

                for i in range(0, len(json_dict["notes"])):
                    data_file = {"id": json_dict["notes"][i]["id"], "title": json_dict["notes"][i]["title"],
                                 "category": json_dict["notes"][i]["category"],
                                 "creation_date": json_dict["notes"][i]["creation_date"],
                                 "last_edit_date": json_dict["notes"][i]["last_edit_date"],
                                 "content": json_dict["notes"][i]["content"]}
                    data_file_dump = json.dumps(data_file)

                    file = open(env + "\\Notepad\\Cache\\" + str(json_dict["notes"][i]["id"]) + ".json", "w+")
                    file.write(data_file_dump)
                    file.close()

    def pushOfflineNotes(self):

        env = os.getenv('APPDATA')

        if db.connected is True:

            for file in os.listdir(env + "\\Notepad\\Cache\\Offline"):
                if file.startswith("offline_"):
                    with open(env + "\\Notepad\\Cache\\Offline\\" + os.path.basename(file), 'r') as content_file:
                        content = content_file.read()
                        json_dict = json.loads(content)

                        self.createNoteAndPush(json_dict["title"], json_dict["category"], json_dict["creation_date"],
                                               json_dict["content"])

                        content_file.close()
                        os.remove(env + "\\Notepad\\Cache\\Offline\\" + os.path.basename(file))

            sql = "SELECT notes FROM notes WHERE account_id= %s"
            val = (self.id,)
            db.cursor.execute(sql, val)
            result = db.cursor.fetchone()

            for file in os.listdir(env + "\\Notepad\\Cache\\Edits"):
                if file.endswith(".json"):
                    with open(env + "\\Notepad\\Cache\\" + os.path.basename(file), 'r') as content_file:
                        content = content_file.read()
                        json_file_dict = json.loads(content)
                        json_db_dict = json.loads(result[0])

                        json_db_dump = json.dumps(json_db_dict["notes"][json_file_dict["id"]])

                        print(result[0])
                        print(content)
                        print(json_db_dump)

                        if (json_file_dict["id"] == json_db_dict["notes"][json_file_dict["id"]]["id"]) and (json_file_dict["title"] == json_db_dict["notes"][json_file_dict["id"]]["title"]) and (json_file_dict["category"] == json_db_dict["notes"][json_file_dict["id"]]["category"]) and (json_file_dict["content"] == json_db_dict["notes"][json_file_dict["id"]]["content"]) and (json_file_dict["last_edit_date"] == json_db_dict["notes"][json_file_dict["id"]]["last_edit_date"]):

                            self.editNote(json_file_dict["id"], json_file_dict["title"], json_file_dict["category"], json_file_dict["last_edit_date"], json_file_dict["content"])
                            content_file.close()
                            os.remove(env + "\\Notepad\\Cache\\Edits\\" + str(json_file_dict["id"]) + ".json")

                        else:

                            print("La note a été modifiée depuis un autre poste")

    def createNoteAndPush(self, title, category_id, current_date, content):

        env = os.getenv('APPDATA')

        if not os.path.exists(env + r'\Notepad'):
            os.makedirs(env + r'\Notepad')
        if not os.path.exists(env + r'\Notepad\Cache'):
            os.makedirs(env + r'\Notepad\Cache')

        if db.connected is True:

            sql = "SELECT notes FROM notes WHERE account_id= %s"
            val = (self.id,)
            db.cursor.execute(sql, val)
            result = db.cursor.fetchone()

            if result is None:

                id = 0

                data = {"notes": [{"id": id, "title": title, "category": category_id, "creation_date": current_date,
                                   "last_edit_date": current_date, "content": content}]}
                data_dump = json.dumps(data)

                print(data_dump)

                sql = "INSERT INTO `notes`(`account_id`, `notes`) VALUES (%s, %s)"
                val = (self.id, data_dump)

                db.cursor.execute(sql, val)
                db.db.commit()

                data_file = {"id": id, "title": title, "category": category_id, "creation_date": current_date,
                             "last_edit_date": current_date, "content": content}
                data_file_dump = json.dumps(data_file)

                file = open(env + "\\Notepad\\Cache\\" + str(id) + ".json", "w+")
                file.write(data_file_dump)
                file.close()

            else:

                current_notes = self.loadNotes()

                last_note = current_notes[(len(current_notes) - 1)]

                id = last_note.id + 1

                data = {"id": id, "title": title, "category": category_id, "creation_date": current_date,
                        "last_edit_date": current_date, "content": content}

                json_dict = json.loads(result[0])
                json_dict["notes"].append(data)

                print(json_dict["notes"].append(data))
                print(data)

                json_dump = json.dumps(json_dict)

                print(json_dump)

                sql = "UPDATE notes SET notes = %s WHERE account_id = %s"
                val = (json_dump, self.id)

                db.cursor.execute(sql, val)
                db.db.commit()

                data_file = {"id": id, "title": title, "category": category_id, "creation_date": current_date,
                             "last_edit_date": current_date, "content": content}
                data_file_dump = json.dumps(data_file)

                file = open(env + "\\Notepad\\Cache\\" + str(id) + ".json", "w+")
                file.write(data_file_dump)
                file.close()

        else:

            if not os.path.exists(env + r'\Notepad\Cache\Offline'):
                os.makedirs(env + r'\Notepad\Cache\Offline')

            offline_id = random.randint(0, 999999)

            while os.path.isfile(env + "\\Notepad\\Cache\\Offline\\" + str(offline_id) + ".json"):
                offline_id = random.randint(0, 999999)

            data_file = {"id": "offline_" + str(offline_id), "title": title, "category": category_id, "creation_date": current_date,
                        "last_edit_date": current_date, "content": content}
            data_file_dump = json.dumps(data_file)

            file = open(env + "\\Notepad\\Cache\\Offline\\offline_" + str(offline_id) + ".json", "w+")
            file.write(data_file_dump)
            file.close()

    def editNote(self, id, title, category_id, current_date, content):

        noteList = self.loadNotes()

        note = Note.getNoteById(id, noteList)
        note.title = title
        note.category = category_id
        note.last_edit_date = current_date
        note.content = content

        if db.connected is True:

            sql = "SELECT notes FROM notes WHERE account_id= %s"
            val = (self.id,)
            db.cursor.execute(sql, val)
            result = db.cursor.fetchone()

            json_dict = json.loads(result[0])
            json_dict["notes"][id]["title"] = title
            json_dict["notes"][id]["category"] = category_id
            json_dict["notes"][id]["last_edit_date"] = current_date
            json_dict["notes"][id]["content"] = content

            json_dump = json.dumps(json_dict)

            sql = "UPDATE notes SET notes = %s WHERE account_id = %s"
            val = (json_dump, self.id)

            db.cursor.execute(sql, val)
            db.db.commit()

            self.loadNotes()
            self.downloadNotes()

        else:

            env = os.getenv('APPDATA')

            if str(note.id).startswith("offline_"):

                file = open(env + "\\Notepad\\Cache\\Offline\\" + str(note.id) + ".json", "r")

                json_dict = json.loads(file.read())

                print(json_dict["title"])

                json_dict["title"] = title
                json_dict["category"] = category_id
                json_dict["last_edit_date"] = current_date
                json_dict["content"] = content

                print(json_dict["title"])

                json_dump = json.dumps(json_dict)

                print(json_dump)

                file = open(env + "\\Notepad\\Cache\\Offline\\" + str(note.id) + ".json", "w+")

                file.write(json_dump)
                file.close()

            else:

                if not os.path.exists(env + r'\Notepad\Cache\Edits'):
                    os.makedirs(env + r'\Notepad\Cache\Edits')

                file = open(env + "\\Notepad\\Cache\\" + str(note.id) + ".json", "r")

                json_dict = json.loads(file.read())

                json_dict["title"] = title
                json_dict["category"] = category_id
                json_dict["last_edit_date"] = current_date
                json_dict["content"] = content

                json_dump = json.dumps(json_dict)

                file.close()

                edit_file = open(env + "\\Notepad\\Cache\\Edits\\" + str(note.id) + ".json", "w+")

                edit_file.write(json_dump)
                edit_file.close()
