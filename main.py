from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "studentos_secret_key"


# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect("database.db")
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

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO users (fullname, email, password, role)
            VALUES (?, ?, ?, ?)
            """, (fullname, email, hashed_password, role))

            conn.commit()

            return redirect("/login")

        except:
            return "User already exists"

        finally:
            conn.close()

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users WHERE email=?
        """, (email,))

        user = cursor.fetchone()

        conn.close()

        if user:

            stored_password = user[3]

            if check_password_hash(stored_password, password):

                session["user_id"] = user[0]
                session["fullname"] = user[1]
                session["role"] = user[4]

                if user[4] == "student":
                    return redirect("/student/dashboard")

                elif user[4] == "teacher":
                    return redirect("/teacher/dashboard")

        return "Invalid email or password"

    return render_template("login.html")


# =========================
# STUDENT DASHBOARD
# =========================

@app.route("/student/dashboard")
def student_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "student_dashboard.html",
        fullname=session["fullname"]
    )


# =========================
# TEACHER DASHBOARD
# =========================

@app.route("/teacher/dashboard")
def teacher_dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "teacher_dashboard.html",
        fullname=session["fullname"]
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
