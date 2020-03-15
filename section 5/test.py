import sqlite3

con = sqlite3.connect("data.db")
cursor = con.cursor()

create_table = "CREATE TABLE users (id INT, username TEXT, password TEXT)"
cursor.execute(create_table)

user = (1, 'sug', '12345')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

us = [
    (2, 'a', '12345'),
    (3, 'b', '12345'),
    (4, 'c', '12345')
]
cursor.executemany(insert_query, us)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

cursor.close()
con.commit()
con.close()
