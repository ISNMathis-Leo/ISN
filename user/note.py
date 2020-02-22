

class Note:


    def __init__(self, id, title, category, creation_date, last_edit_date, content):
        self.id = id
        self.title = title
        self.category = category
        self.creation_date = creation_date
        self.last_edit_date = last_edit_date
        self.content = content

    @classmethod
    def getNoteById(cls, id, notesList):

        for i in range(0, len(notesList)):
            if notesList[i].id == id:
                return notesList[i]