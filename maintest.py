from database.database import Database
from user.user import User


class Main:

    db = Database()
    db.connect()

    User.setDatabase(db)

    user = User.login("cc", "cc")
    notes = user.createNoteAndPush("cc", "cc", "cc", "cc", "cc")
    notes = user.loadNotes()

    #print(notes[3].content)
