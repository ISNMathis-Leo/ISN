class Database :

    def createNewUser(db, name, nickname, encrypted_password, email, notes, abrevs, categories) :



        sql = "INSERT INTO notepad (name, nickname, encrypted_password, email, notes, abrevs, categories) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, nickname, encrypted_password, email, notes, abrevs, categories)
        db.cursor.execute(sql, val)
        db.mydb.commit()
