import sqlite3

conn = sqlite3.connect("helpdesk.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO tickets
(student_name, issue, department, priority, status, created_date)
VALUES
('Aleeza',
 'Forgot LMS Password',
 'IT Support',
 'High',
 'Open',
 '2026-06-21')
""")

conn.commit()
conn.close()

print("Inserted")