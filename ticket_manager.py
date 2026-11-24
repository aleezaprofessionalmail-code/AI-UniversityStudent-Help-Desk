def create_ticket(student_name, issue, department, priority):

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets 
        (student_name, issue, department, priority, status, created_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        issue if issue else "No issue provided",
        department if department else "General",
        priority if priority else "Low",
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()

    return ticket_id