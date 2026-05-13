from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = "edunova_super_secret_key_2026"

# =========================
# USERS FILE (JSON DB)
# =========================
USERS_FILE = "users.json"


# =========================
# LOAD USERS
# =========================
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


# =========================
# SAVE USERS
# =========================
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# =========================
# HOME (SPLASH OR LOGIN)
# =========================
@app.route("/")
def home():
    return redirect(url_for("login"))


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    users = load_users()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and check_password_hash(users[username]["password"], password):
            session["user"] = username
            session["role"] = users[username]["role"]

            flash("Login successful!", "success")

            if users[username]["role"] == "student":
                return redirect(url_for("student_dashboard"))
            else:
                return redirect(url_for("teacher_dashboard"))

        flash("Invalid username or password", "error")

    return render_template("login.html")


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    users = load_users()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        if username in users:
            flash("User already exists!", "error")
            return redirect(url_for("register"))

        # Strong password hashing
        users[username] = {
            "password": generate_password_hash(password),
            "role": role
        }

        save_users(users)

        flash("Account created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# STUDENT DASHBOARD
# =========================
@app.route("/student/dashboard")
def student_dashboard():
    if "user" not in session or session.get("role") != "student":
        return redirect(url_for("login"))

    return render_template("student_dashboard.html", user=session["user"])


# =========================
# TEACHER DASHBOARD
# =========================
@app.route("/teacher/dashboard")
def teacher_dashboard():
    if "user" not in session or session.get("role") != "teacher":
        return redirect(url_for("login"))

    return render_template("teacher_dashboard.html", user=session["user"])


# =========================
# HOMEWORK PAGE
# =========================
@app.route("/homework")
def homework():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("homework.html")


# =========================
# TIMETABLE
# =========================
@app.route("/timetable")
def timetable():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("timetable.html")


# =========================
# CHAT
# =========================
@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("chat.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
