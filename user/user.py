

class User:

    def __init__(self, id, name, nickname, encrypted_password, email, notes, abrevs, categories):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.encrypted_password = encrypted_password
        self.email = email
        self.notes = notes
        self.abrevs = abrevs
        self.categories = categories
