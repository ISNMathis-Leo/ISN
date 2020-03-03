import os


class FileManager:

    env = os.getenv('APPDATA')

    root = env + "\\.notepad"
    cache = env + "\\.notepad\\cache"

    notes = env + "\\.notepad\\cache\\notes"
    edits = env + "\\.notepad\\cache\\edits"
    offline = env + "\\.notepad\\cache\\offline"

    @classmethod
    def checkFiles(cls):

        if not os.path.exists(cls.root):
            os.makedirs(cls.root)
        if not os.path.exists(cls.cache):
            os.makedirs(cls.cache)
        if not os.path.exists(cls.edits):
            os.makedirs(cls.edits)
        if not os.path.exists(cls.offline):
            os.makedirs(cls.offline)
        if not os.path.exists(cls.notes):
            os.makedirs(cls.notes)
