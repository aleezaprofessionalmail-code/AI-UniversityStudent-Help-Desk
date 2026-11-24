import sqlite3

conn = sqlite3.connect("helpdesk.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    issue TEXT,
    department TEXT,
    priority TEXT,
    status TEXT,
    created_date TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")