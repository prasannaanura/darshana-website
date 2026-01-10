import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    checkin DATE NOT NULL,
    checkout DATE NOT NULL
)
""")

conn.commit()
conn.close()

print("Database initialized successfully.")
