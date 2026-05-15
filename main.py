from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = "eduflow_ultra_secret_2026"

# =========================================
# DATA FOLDER
# =========================================
DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# =========================================
# FILE PATHS
# =========================================
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
HOMEWORK_FILE = os.path.join(DATA_FOLDER, "homework.json")
RESULT_FILE = os.path.join(DATA_FOLDER, "results.json")

# =========================================
# CREATE FILES IF NOT EXIST
# =========================================
for file in [USERS_FILE, HOMEWORK_FILE, RESULT_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

# =========================================
# LOAD JSON
# =========================================
def load_json(file):

    with open(file, "r") as f:
        try:
            return json.load(f)
        except:
            return []

# =========================================
# SAVE JSON
# =========================================
def save_json(file, data):

    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# =========================================
# HOME
# =========================================
@app.route("/")
def home():
    return redirect(url_for("login"))

# =========================================
# REGISTER
# =========================================
@app.route("/register", methods=["GET", "POST"])
def register():

    users = load_json(USERS_FILE)

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # CHECK IF USER EXISTS
        for user in users:
            if user["email"] == email:
                flash("Account already exists!", "danger")
                return redirect(url_for("register"))

        new_user = {
            "fullname": fullname,
            "email": email,
            "password": generate_password_hash(password),
            "role": role
        }

        users.append(new_user)

        save_json(USERS_FILE, users)

        flash("Registration successful!", "success")

        return redirect(url_for("login"))

    return render_template("register.html")

# =========================================
# LOGIN
# =========================================
@app.route("/login", methods=["GET", "POST"])
def login():

    users = load_json(USERS_FILE)

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        for user in users:

            if user["email"] == email and check_password_hash(user["password"], password):

                session["user"] = user["fullname"]
                session["email"] = user["email"]
                session["role"] = user["role"]

                flash("Login successful!", "success")

                # REDIRECT BY ROLE
                if user["role"] == "student":
                    return redirect(url_for("student_dashboard"))

                elif user["role"] == "teacher":
                    return redirect(url_for("teacher_dashboard"))

                elif user["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))

        flash("Invalid email or password", "danger")

    return render_template("login.html")

# =========================================
# STUDENT DASHBOARD
# =========================================
@app.route("/student/dashboard")
def student_dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    if session["role"] != "student":
        return redirect(url_for("login"))

    return render_template(
        "student_dashboard.html",
        user=session["user"]
    )

# =========================================
# TEACHER DASHBOARD
# =========================================
@app.route("/teacher/dashboard")
def teacher_dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    if session["role"] != "teacher":
        return redirect(url_for("login"))

    return render_template(
        "teacher_dashboard.html",
        user=session["user"]
    )

# =========================================
# ADMIN DASHBOARD
# =========================================
@app.route("/admin/dashboard")
def admin_dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return redirect(url_for("login"))

    users = load_json(USERS_FILE)
    homework = load_json(HOMEWORK_FILE)
    results = load_json(RESULT_FILE)

    student_count = len([u for u in users if u["role"] == "student"])
    teacher_count = len([u for u in users if u["role"] == "teacher"])

    return render_template(
        "admin_dashboard.html",
        user=session["user"],
        students=student_count,
        teachers=teacher_count,
        homework_count=len(homework),
        results_count=len(results)
    )

# =========================================
# HOMEWORK
# =========================================
@app.route("/homework", methods=["GET", "POST"])
def homework():

    if "user" not in session:
        return redirect(url_for("login"))

    homework_data = load_json(HOMEWORK_FILE)

    # TEACHER POST HOMEWORK
    if request.method == "POST":

        if session["role"] != "teacher":
            flash("Only teachers can upload homework", "danger")
            return redirect(url_for("homework"))

        title = request.form["title"]
        subject = request.form["subject"]
        description = request.form["description"]

        new_homework = {
            "title": title,
            "subject": subject,
            "description": description,
            "teacher": session["user"]
        }

        homework_data.append(new_homework)

        save_json(HOMEWORK_FILE, homework_data)

        flash("Homework uploaded!", "success")

        return redirect(url_for("homework"))

    return render_template(
        "homework.html",
        homeworks=homework_data,
        role=session["role"]
    )

# =========================================
# RESULTS
# =========================================
@app.route("/results", methods=["GET", "POST"])
def results():

    if "user" not in session:
        return redirect(url_for("login"))

    results_data = load_json(RESULT_FILE)

    # TEACHER ADD RESULT
    if request.method == "POST":

        if session["role"] != "teacher":
            flash("Only teachers can upload results", "danger")
            return redirect(url_for("results"))

        student = request.form["student"]
        subject = request.form["subject"]
        score = request.form["score"]

        new_result = {
            "student": student,
            "subject": subject,
            "score": score,
            "teacher": session["user"]
        }

        results_data.append(new_result)

        save_json(RESULT_FILE, results_data)

        flash("Result uploaded successfully!", "success")

        return redirect(url_for("results"))

    return render_template(
        "results.html",
        results=results_data,
        role=session["role"]
    )

# =========================================
# TIMETABLE
# =========================================
@app.route("/timetable")
def timetable():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("timetable.html")

# =========================================
# CHAT
# =========================================
@app.route("/chat")
def chat():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "chat.html",
        user=session["user"]
    )

# =========================================
# LOGOUT
# =========================================
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "success")

    return redirect(url_for("login"))

# =========================================
# RUN APP
# =========================================
if __name__ == "__main__":
    app.run(debug=True)
