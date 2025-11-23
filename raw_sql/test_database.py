import sqlite3

conn = sqlite3.connect("app.db")  # use the same name as in db_init.py
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

conn.close()
