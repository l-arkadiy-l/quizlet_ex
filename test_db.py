import sqlite3
user_id = 680009374
f = open('3.png')
conn = sqlite3.connect('users.db')

c = conn.cursor()
# c.execute("CREATE TABLE users (id integer UNIQUE, path text)")
try:
    c.execute(f"INSERT INTO users VALUES ({user_id}, 'pathxl/{user_id}.xlsx')")
    conn.commit()
except sqlite3.IntegrityError:
    pass
c.execute(f"SELECT * FROM users WHERE id={user_id}")
print(c.fetchone())
c.close()