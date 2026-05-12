from flask import Flask, render_template, request
import sqlite3
import os
from werkzeug.utils import secure_filename

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
        fullname TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# SPLASH SCREEN
# =========================

@app.route("/")
def splash():
    return render_template("splash.html")

# =========================
# WELCOME PAGE
# =========================

@app.route("/welcome")
def welcome():
    return render_template("index.html")

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

        conn = sqlite3.connect("studentos.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users (fullname, email, password, role)
        VALUES (?, ?, ?, ?)
        """, (fullname, email, password, role))

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

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

        cursor.execute("""
        SELECT * FROM users
        WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            role = user[4]

            if role == "Teacher":
                return redirect(url_for("teacher_dashboard"))

            else:
                return redirect(url_for("student_dashboard"))

        else:
            return "Invalid Login Details"

    return render_template("login.html")

# =========================
# STUDENT DASHBOARD
# =========================

@app.route("/student_dashboard")
def student_dashboard():
    return render_template("Student_dashboard.html")

# =========================
# TEACHER DASHBOARD
# =========================

@app.route("/teacher_dashboard")
def teacher_dashboard():
    return render_template("teacher_dashboard.html")
# =========================
# HOMEWORK UPLOAD
# =========================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/homework", methods=["GET", "POST"])
def homework():

    if request.method == "POST":

        subject = request.form["subject"]

        file = request.files["homework"]

        if file:

            filename = secure_filename(file.filename)

            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            return f"Homework uploaded successfully for {subject}"

    return render_template("homework.html")
# =========================
# RUN APP
# =========================

if __name__ == "__main__":
app.run(host="0.0.0.0", port=5000)
