from database.database import Database
from user.user import User
from files.filemanager import FileManager


class Main:

    db = Database()
    db.connect()

    User.setDatabase(db)

    user = User.login("cc", "cc")

    FileManager.checkFiles()

    user.pushOfflineNotes()
    user.downloadNotes()
    notesList = user.loadNotes()

    # user.createNoteAndPush("cc", "cc", "cc", "cc")

    user.editNote(0, "bg", 2, "michel", "bonjour")

    for i in range(0, len(notesList)):
        print("")
        print(notesList[i].id)
        print(notesList[i].title)
        print(notesList[i].content)
        print(notesList[i].category)
        print(notesList[i].creation_date)

    # print(notes[3].content)
