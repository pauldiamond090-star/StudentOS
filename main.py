from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = "edunova_secret_2026"

# =========================================
# DATA FOLDER
# =========================================
DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
HOMEWORK_FILE = os.path.join(DATA_FOLDER, "homework.json")
SCHOOLS_FILE = os.path.join(DATA_FOLDER, "schools.json")


# =========================================
# CREATE FILES
# =========================================
def create_file(file, default_data):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump(default_data, f, indent=4)


create_file(USERS_FILE, [])
create_file(HOMEWORK_FILE, [])
create_file(SCHOOLS_FILE, [])


# =========================================
# LOAD JSON
# =========================================
def load_json(file):
    try:
        with open(file, "r") as f:
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
    schools = load_json(SCHOOLS_FILE)

    if request.method == "POST":

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        school_name = request.form.get("school")

        # CHECK EXISTING USER
        for user in users:
            if user["email"] == email:
                flash("Account already exists!", "danger")
                return redirect(url_for("register"))

        # CREATE USER
        new_user = {
            "fullname": fullname,
            "email": email,
            "password": generate_password_hash(password),
            "role": role,
            "school": school_name
        }

        users.append(new_user)
        save_json(USERS_FILE, users)

        flash("Account created successfully!", "success")

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        schools=schools
    )


# =========================================
# LOGIN
# =========================================
@app.route("/login", methods=["GET", "POST"])
def login():

    users = load_json(USERS_FILE)

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        for user in users:

            if (
                user["email"] == email
                and check_password_hash(user["password"], password)
            ):

                session["user"] = user["email"]
                session["fullname"] = user["fullname"]
                session["role"] = user["role"]
                session["school"] = user["school"]

                flash("Login successful!", "success")

                if user["role"] == "student":
                    return redirect(url_for("student_dashboard"))

                elif user["role"] == "teacher":
                    return redirect(url_for("teacher_dashboard"))

                elif user["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))

                elif user["role"] == "school_admin":
                    return redirect(url_for("school_admin_dashboard"))

        flash("Invalid email or password!", "danger")

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

    homework = load_json(HOMEWORK_FILE)

    return render_template(
        "student_dashboard.html",
        user=session["fullname"],
        homework=homework
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

    homework = load_json(HOMEWORK_FILE)

    return render_template(
        "teacher_dashboard.html",
        user=session["fullname"],
        homework=homework
    )


# =========================================
# MAIN ADMIN DASHBOARD
# =========================================
@app.route("/admin/dashboard")
def admin_dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return redirect(url_for("login"))

    users = load_json(USERS_FILE)
    schools = load_json(SCHOOLS_FILE)

    return render_template(
        "admin_dashboard.html",
        user=session["fullname"],
        users=users,
        schools=schools
    )


# =========================================
# SCHOOL ADMIN DASHBOARD
# =========================================
@app.route("/school-admin/dashboard")
def school_admin_dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    if session["role"] != "school_admin":
        return redirect(url_for("login"))

    users = load_json(USERS_FILE)

    school_students = []
    school_teachers = []

    for user in users:

        if user["school"] == session["school"]:

            if user["role"] == "student":
                school_students.append(user)

            elif user["role"] == "teacher":
                school_teachers.append(user)

    return render_template(
        "school_admin_dashboard.html",
        user=session["fullname"],
        school=session["school"],
        students=school_students,
        teachers=school_teachers
    )


# =========================================
# ADD SCHOOL
# =========================================
@app.route("/add-school", methods=["POST"])
def add_school():

    if "user" not in session:
        return redirect(url_for("login"))

    if session["role"] != "admin":
        return redirect(url_for("login"))

    schools = load_json(SCHOOLS_FILE)

    school_name = request.form.get("school_name")

    new_school = {
        "name": school_name
    }

    schools.append(new_school)

    save_json(SCHOOLS_FILE, schools)

    flash("School added successfully!", "success")

    return redirect(url_for("admin_dashboard"))


# =========================================
# ADD HOMEWORK
# =========================================
@app.route("/add-homework", methods=["GET", "POST"])
def add_homework():

    if "user" not in session:
        return redirect(url_for("login"))

    if session["role"] != "teacher":
        return redirect(url_for("login"))

    homework = load_json(HOMEWORK_FILE)

    if request.method == "POST":

        title = request.form.get("title")
        subject = request.form.get("subject")
        description = request.form.get("description")
        deadline = request.form.get("deadline")

        new_homework = {
            "title": title,
            "subject": subject,
            "description": description,
            "deadline": deadline,
            "teacher": session["fullname"],
            "school": session["school"]
        }

        homework.append(new_homework)

        save_json(HOMEWORK_FILE, homework)

        flash("Homework uploaded!", "success")

        return redirect(url_for("teacher_dashboard"))

    return render_template("upload_homework.html")


# =========================================
# HOMEWORK PAGE
# =========================================
@app.route("/homework")
def homework_page():

    if "user" not in session:
        return redirect(url_for("login"))

    homework = load_json(HOMEWORK_FILE)

    return render_template(
        "homework.html",
        homework=homework
    )


# =========================================
# CHAT
# =========================================
@app.route("/chat")
def chat():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("chat.html")


# =========================================
# TIMETABLE
# =========================================
@app.route("/timetable")
def timetable():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("timetable.html")


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
