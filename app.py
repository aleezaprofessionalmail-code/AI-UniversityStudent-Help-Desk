from flask import Flask, jsonify, request, render_template, session, redirect
from ai_engine import get_solution
from ticket_manager import create_ticket
import sqlite3
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY is missing. Please configure your .env file.")


# ==========================
# DATABASE
# ==========================

# ==========================
# DATABASE FUNCTIONS
# ==========================

def create_database():

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    # USERS TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # TICKETS TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        issue TEXT,
        department TEXT,
        priority TEXT,
        status TEXT,
        created_date TEXT
    )
    """)

    # DEFAULT ADMIN

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (id, username, password, role)
    VALUES
    (1, 'admin', '123', 'admin')
    """)

    # DEFAULT STUDENT

    cursor.execute("""
    INSERT OR IGNORE INTO users
    (id, username, password, role)
    VALUES
    (2, 'student', '123', 'student')
    """)

     # Migrate existing plain-text passwords to secure hashes
    cursor.execute("SELECT id, password FROM users")
    users = cursor.fetchall()

    for user_id, password in users:
        if password and not password.startswith(("scrypt:", "pbkdf2:")):
            hashed_password = generate_password_hash(password)

            cursor.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (hashed_password, user_id)
            )

    conn.commit()
    conn.close()


def save_user(username, password, role):

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users(username,password,role)
    VALUES(?,?,?)
    """, (username, password, role))

    conn.commit()
    conn.close()


def get_user(username, password):

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, role
    FROM users
    WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    return user


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        data = request.get_json()

        username = data["username"]
        password = data["password"]

        conn = sqlite3.connect("helpdesk.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT username, password, role
        FROM users
        WHERE username=?
        """, (username,))

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):

            session["username"] = user[0]
            session["role"] = user[2]

            if user[2] == "admin":
                redirect_url = "/admin"
            else:
                redirect_url = "/dashboard"

            return jsonify({
                "success": True,
                "role": user[2],
                "redirect": redirect_url
            })

        return jsonify({"success": False})

    return render_template("login.html")
# ==========================
# SIGNUP
# ==========================


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    username = request.form['username']
    password = request.form['password']
                  
    hashed_password = generate_password_hash(password)
    role = request.form['role']

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE username = ?
    """, (username,))
    
    if cursor.fetchone():
        return "User already exists", 400

        cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
    """, (username, hashed_password, role))

    conn.commit()
    conn.close()

    return redirect('/login')
# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")

    return render_template("dashboard.html")

# ==========================
# CHATBOT API
# ==========================

@app.route("/chat", methods=["POST"])
def chat():

    if "username" not in session:
        return jsonify({"found": False, "message": "Please login first"})

    data = request.get_json()
    query = data.get("query")

    result = get_solution(query)

    return jsonify({
        "found": True,
        "department": result.get("department", "General Support"),
        "solution": result.get("solution", result.get("message", "No solution")),
        "priority": result.get("priority", "Low")
    })


# ==========================
# CREATE TICKET
# ==========================

@app.route("/create_ticket", methods=["POST"])
def create_new_ticket():

    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    # 🔥 DEBUG HERE (RIGHT PLACE)
    print("DEBUG TICKET DATA:", data)

    ticket_id = create_ticket(
        session["username"],
        data.get("issue"),
        data.get("department"),
        data.get("priority")
    )

    return jsonify({
        "ticket_id": ticket_id,
        "status": "Open"
    })
# ==========================
# GET ALL TICKETS
# ==========================

@app.route("/api/tickets")
def get_tickets():

    if "username" not in session:
        return jsonify([])

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM tickets
    WHERE student_name = ?
    ORDER BY id DESC
    """, (session["username"],))

    rows = cursor.fetchall()
    conn.close()

    tickets = []

    for r in rows:
        tickets.append({
            "id": r[0],
            "student_name": r[1],
            "issue": r[2],
            "department": r[3],
            "priority": r[4],
            "status": r[5],
            "created_date": r[6],
            "ticket_id": f"SMIU-2026-{str(r[0]).zfill(4)}"
        })

    return jsonify(tickets)

# ==========================
# TICKETS PAGE
# ==========================

@app.route("/tickets")
def tickets_page():

    if "username" not in session:
        return redirect("/login")

    return render_template("tickets.html")


# ==========================
# CHATBOT PAGE
# ==========================

@app.route("/chatbot")
def chatbot_page():

    if "username" not in session:
        return redirect("/login")

    return render_template("chatbot.html")


# ==========================
# ADMIN PAGE
# ==========================

@app.route("/admin")
def admin_page():

    if session.get("role") != "admin":
        return redirect("/login")

    return render_template("admin.html")


@app.route("/api/admin/tickets")
def admin_tickets():

    if session.get("role") != "admin":
        return jsonify([])

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM tickets
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    tickets = []

    for r in rows:
        tickets.append({
            "id": r[0],
            "student_name": r[1],
            "issue": r[2],
            "department": r[3],
            "priority": r[4],
            "status": r[5],
            "created_date": r[6]
        })

    return jsonify(tickets)


@app.route("/resolve_ticket/<int:ticket_id>", methods=["POST"])
def resolve_ticket(ticket_id):

    if session.get("role") != "admin":
        return jsonify({"success": False})

    conn = sqlite3.connect("helpdesk.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tickets
    SET status='Resolved'
    WHERE id=?
    """, (ticket_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True
    })

# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":

    create_database()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )