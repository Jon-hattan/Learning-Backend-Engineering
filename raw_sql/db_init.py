"""
Initialises the database
"""


import sqlite3

DB_PATH = "app.db"

conn = sqlite3.connect(DB_PATH) # open connection to database
cur = conn.cursor() # query executor and result iterator

# use this to execute the SQL queries
cur.executescript(
    """
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        text   TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """
)

conn.commit()
conn.close()
print(f"Database initialised at {DB_PATH}")