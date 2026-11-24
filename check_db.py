import sqlite3

conn = sqlite3.connect("helpdesk.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM tickets")

print(cursor.fetchall())

conn.close()