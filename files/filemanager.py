import os


class FileManager:
    env = os.getenv('APPDATA')

    root = env + "\\.notepad"
    logs = env + "\\.notepad\\logs"
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
        if not os.path.exists(cls.logs):
            os.makedirs(cls.logs)

    @classmethod
    def get_all_file_paths(cls, directory):

        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        return file_paths
