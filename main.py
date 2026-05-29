from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json
import os

# =========================================
# APP CONFIG
# =========================================
app = Flask(__name__)

app.secret_key = "edunova_secret_2026"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================================
# FOLDERS
# =========================================
DATA_FOLDER = "data"
UPLOAD_FOLDER = "uploads"

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =========================================
# FILES
# =========================================
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
HOMEWORK_FILE = os.path.join(DATA_FOLDER, "homework.json")
SCHOOLS_FILE = os.path.join(DATA_FOLDER, "schools.json")
EXAMS_FILE = os.path.join(DATA_FOLDER, "exams.json")
RESULTS_FILE = os.path.join(DATA_FOLDER, "results.json")
MESSAGES_FILE = os.path.join(DATA_FOLDER, "messages.json")
GRADES_FILE = os.path.join(DATA_FOLDER, "grades.json")
SUBSCRIPTIONS_FILE = os.path.join(DATA_FOLDER, "subscriptions.json")

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
create_file(EXAMS_FILE, [])
create_file(RESULTS_FILE, [])
create_file(MESSAGES_FILE, [])
create_file(GRADES_FILE, [])
create_file(SUBSCRIPTIONS_FILE, [])

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
# DATABASE MODELS
# =========================================
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(200), nullable=False)

    email = db.Column(db.String(200), unique=True, nullable=False)

    password = db.Column(db.String(300), nullable=False)

    role = db.Column(db.String(50), nullable=False)

    school = db.Column(db.String(200))

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


class School(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), unique=True, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


class Homework(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    subject = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    deadline = db.Column(db.String(100))

    teacher = db.Column(db.String(200))

    school = db.Column(db.String(200))

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


class Exam(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    subject = db.Column(db.String(200), nullable=False)

    question = db.Column(db.Text)

    option_a = db.Column(db.String(300))

    option_b = db.Column(db.String(300))

    option_c = db.Column(db.String(300))

    option_d = db.Column(db.String(300))

    correct_answer = db.Column(db.String(100))

    teacher = db.Column(db.String(200))

    school = db.Column(db.String(200))

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


class Result(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student = db.Column(db.String(200))

    exam_title = db.Column(db.String(200))

    subject = db.Column(db.String(200))

    score = db.Column(db.Integer)

    school = db.Column(db.String(200))

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


class Grade(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student = db.Column(db.String(200))

    subject = db.Column(db.String(200))

    score = db.Column(db.String(100))

    remark = db.Column(db.String(300))

    teacher = db.Column(db.String(200))

    school = db.Column(db.String(200))

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    sender = db.Column(db.String(200))

    role = db.Column(db.String(100))

    school = db.Column(db.String(200))

    message = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )


class Subscription(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    school = db.Column(db.String(200))

    plan = db.Column(db.String(100))

    status = db.Column(db.String(100))

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

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

        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        school = request.form.get("school")

        for user in users:

            if user["email"] == email:

                flash("Account already exists!", "danger")
                return redirect(url_for("register"))

        new_user = {
            "fullname": fullname,
            "email": email,
            "password": generate_password_hash(password),
            "role": role,
            "school": school
        }

        users.append(new_user)

        save_json(USERS_FILE, users)

        flash("Account created successfully!", "success")

        return redirect(url_for("login"))

    schools = load_json(SCHOOLS_FILE)

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
                user["email"] == email and
                check_password_hash(user["password"], password)
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

        flash("Invalid login details!", "danger")

    return render_template("login.html")

# =========================================
# STUDENT DASHBOARD
# =========================================
@app.route("/student/dashboard")
def student_dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "student_dashboard.html",
        user=session["fullname"]
    )

# =========================================
# TEACHER DASHBOARD
# =========================================
@app.route("/teacher/dashboard")
def teacher_dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "teacher_dashboard.html",
        user=session["fullname"]
    )

# =========================================
# ADMIN DASHBOARD
# =========================================
@app.route("/admin/dashboard")
def admin_dashboard():

    if "user" not in session:
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

    return render_template(
        "school_admin_dashboard.html",
        user=session["fullname"]
    )

# =========================================
# LOGOUT
# =========================================
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out!", "success")

    return redirect(url_for("login"))

# =========================================
# RUN APP
# =========================================
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)
