from database.database import Database
from user.user import User


class Main:

    db = Database()
    db.connect()

    User.setDatabase(db)

    user = User.login("cc", "cc")

    user.pushOfflineNotes()
    notesList = user.loadNotes()
    user.downloadNotes()

    # user.createNoteAndPush("cc", "cc", "cc", "cc")

    user.editNote(0, "bg", 2, "michel", "bisou22222s")


    for i in range(0, len(notesList)):
        print("")
        print(notesList[i].id)
        print(notesList[i].title)
        print(notesList[i].content)
        print(notesList[i].category)
        print(notesList[i].creation_date)

    #print(notes[3].content)
