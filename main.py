from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)

# =========================
# DATABASE SETUP
# =========================

def init_db():
    conn = sqlite3.connect("studentos.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
        <title>StudentOS</title>
    </head>
    <body style="font-family: Arial; padding: 40px;">

        <h1>Welcome to StudentOS</h1>

        <a href="/register">
            <button>Register</button>
        </a>

        <a href="/login">
            <button>Login</button>
        </a>

    </body>
    </html>
    """)

# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        try:
            conn = sqlite3.connect("studentos.db")
            cursor = conn.cursor()

            # Check existing email
            cursor.execute(
                "SELECT * FROM users WHERE email = ?",
                (email,)
            )

            existing_user = cursor.fetchone()

            if existing_user:
                conn.close()
                return "Email already exists."

            # Insert user
            cursor.execute(
                "INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)",
                (fullname, email, password, role)
            )

            conn.commit()
            conn.close()

            return redirect("/login")

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template_string("""
    <html>
    <head>
        <title>Register</title>
    </head>
    <body style="font-family: Arial; padding: 40px;">

        <h2>Create Account</h2>

        <form method="POST">

            <input type="text" name="fullname" placeholder="Full Name" required>
            <br><br>

            <input type="email" name="email" placeholder="Email" required>
            <br><br>

            <input type="password" name="password" placeholder="Password" required>
            <br><br>

            <select name="role">
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
            </select>

            <br><br>

            <button type="submit">Register</button>

        </form>

    </body>
    </html>
    """)

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("studentos.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            role = user[4]

            if role == "student":
                return redirect("/student_dashboard")

            else:
                return redirect("/teacher_dashboard")

        else:
            return "Invalid login details."

    return render_template_string("""
    <html>
    <head>
        <title>Login</title>
    </head>
    <body style="font-family: Arial; padding: 40px;">

        <h2>Login</h2>

        <form method="POST">

            <input type="email" name="email" placeholder="Email" required>
            <br><br>

            <input type="password" name="password" placeholder="Password" required>
            <br><br>

            <button type="submit">Login</button>

        </form>

    </body>
    </html>
    """)

# =========================
# STUDENT DASHBOARD
# =========================

@app.route("/student_dashboard")
def student_dashboard():

    return render_template_string("""
    <html>
    <head>
        <title>Student Dashboard</title>
    </head>
    <body style="font-family: Arial; padding: 40px;">

        <h1>Student Dashboard</h1>

        <ul>
            <li>Homework</li>
            <li>Exam Results</li>
            <li>Timetable</li>
            <li>Attendance</li>
        </ul>

    </body>
    </html>
    """)

# =========================
# TEACHER DASHBOARD
# =========================

@app.route("/teacher_dashboard")
def teacher_dashboard():

    return render_template_string("""
    <html>
    <head>
        <title>Teacher Dashboard</title>
    </head>
    <body style="font-family: Arial; padding: 40px;">

        <h1>Teacher Dashboard</h1>

        <ul>
            <li>Upload Homework</li>
            <li>Manage Students</li>
            <li>Upload Results</li>
            <li>Create Timetable</li>
        </ul>

    </body>
    </html>
    """)

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
