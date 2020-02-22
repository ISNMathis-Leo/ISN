from database.database import Database
from user.user import User


class Main:

    db = Database()
    db.connect()

    User.setDatabase(db)

    user = User.login("cc", "cc")

    # user.createNoteAndPush("cc", "cc", "cc", "cc")

    user.pushOfflineNotes()
    notes = user.loadNotes()
    user.downloadNotes()


    for i in range(0, len(notes)):
        print("")
        print(notes[i].id)
        print(notes[i].title)
        print(notes[i].content)
        print(notes[i].category)
        print(notes[i].creation_date)

    #print(notes[3].content)
