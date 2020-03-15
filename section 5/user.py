import sqlite3


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)

        else:
            user = None

        cursor.close()
        con.close()
        return user

    @classmethod
    def find_by_userid(cls, user_id):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (user_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)

        else:
            user = None

        cursor.close()
        con.close()
        return user
