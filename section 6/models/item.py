import sqlite3


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    def update(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cur.execute(query, (self.price, self.name))

        cur.close()
        con.commit()
        con.close()

    def insert(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cur.execute(query, (self.name, self.price))

        cur.close()
        con.commit()
        con.close()

    @classmethod
    def find_by_name(cls, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items WHERE name=?"
        res = cur.execute(query, (name,))
        row = res.fetchone()
        cur.close()
        con.close()
        if row:
            return cls(*row)
