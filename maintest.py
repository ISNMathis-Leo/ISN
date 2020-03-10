from database.database import Database
from user.user import User
from files.filemanager import FileManager
from files.logs import Log

class Main:

    FileManager.checkFiles()
    Log.init()

    Log.info("Checking files...")
    Log.info("Files OK")

    Log.info("Database connection test...")
    db = Database()
    db.connect()

    User.setDatabase(db)

    user = User.login("cc", "cc")

    user.pushOfflineNotes()
    user.downloadNotes()
    notesList = user.loadNotes()
