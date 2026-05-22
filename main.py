from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
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

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =========================================
# DATABASE FILES
# =========================================
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
HOMEWORK_FILE = os.path.join(DATA_FOLDER, "homework.json")
SCHOOLS_FILE = os.path.join(DATA_FOLDER, "schools.json")
EXAMS_FILE = os.path.join(DATA_FOLDER, "exams.json")
RESULTS_FILE = os.path.join(DATA_FOLDER, "results.json")


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

        for user in users:

            if user["email"] == email:

                flash("Account already exists!", "danger")

                return redirect(url_for("register"))

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

    return render_template(
        "teacher_dashboard.html",
        user=session["fullname"]
    )


# =========================================
# MAIN ADMIN DASHBOARD
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

    users = load_json(USERS_FILE)

    students = []
    teachers = []

    for user in users:

        if user["school"] == session["school"]:

            if user["role"] == "student":
                students.append(user)

            elif user["role"] == "teacher":
                teachers.append(user)

    return render_template(
        "school_admin_dashboard.html",
        user=session["fullname"],
        students=students,
        teachers=teachers,
        school=session["school"]
    )


# =========================================
# ADD SCHOOL
# =========================================
@app.route("/add-school", methods=["POST"])
def add_school():

    if "user" not in session:
        return redirect(url_for("login"))

    schools = load_json(SCHOOLS_FILE)

    school_name = request.form.get("school_name")

    new_school = {
        "name": school_name
    }

    schools.append(new_school)

    save_json(SCHOOLS_FILE, schools)

    flash("School added!", "success")

    return redirect(url_for("admin_dashboard"))


# =========================================
# ADD HOMEWORK
# =========================================
@app.route("/add-homework", methods=["GET", "POST"])
def add_homework():

    if "user" not in session:
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
# CREATE EXAM
# =========================================
@app.route("/create-exam", methods=["GET", "POST"])
def create_exam():

    if "user" not in session:
        return redirect(url_for("login"))

    exams = load_json(EXAMS_FILE)

    if request.method == "POST":

        title = request.form.get("title")
        subject = request.form.get("subject")
        question = request.form.get("question")

        option_a = request.form.get("option_a")
        option_b = request.form.get("option_b")
        option_c = request.form.get("option_c")
        option_d = request.form.get("option_d")

        correct_answer = request.form.get("correct_answer")

        new_exam = {
            "id": len(exams) + 1,
            "title": title,
            "subject": subject,
            "question": question,
            "option_a": option_a,
            "option_b": option_b,
            "option_c": option_c,
            "option_d": option_d,
            "correct_answer": correct_answer,
            "teacher": session["fullname"],
            "school": session["school"]
        }

        exams.append(new_exam)

        save_json(EXAMS_FILE, exams)

        flash("Exam created successfully!", "success")

        return redirect(url_for("teacher_dashboard"))

    return render_template("create_exam.html")


# =========================================
# VIEW EXAMS
# =========================================
@app.route("/exams")
def exams():

    if "user" not in session:
        return redirect(url_for("login"))

    exams = load_json(EXAMS_FILE)

    school_exams = []

    for exam in exams:

        if exam["school"] == session["school"]:
            school_exams.append(exam)

    return render_template(
        "exams.html",
        exams=school_exams
    )


# =========================================
# TAKE EXAM
# =========================================
@app.route("/take-exam/<int:exam_id>", methods=["GET", "POST"])
def take_exam(exam_id):

    if "user" not in session:
        return redirect(url_for("login"))

    exams = load_json(EXAMS_FILE)
    results = load_json(RESULTS_FILE)

    selected_exam = None

    for exam in exams:

        if exam["id"] == exam_id:
            selected_exam = exam
            break

    if selected_exam is None:

        flash("Exam not found!", "danger")

        return redirect(url_for("exams"))

    if request.method == "POST":

        answer = request.form.get("answer")

        score = 0

        if answer == selected_exam["correct_answer"]:
            score = 100

        result = {
            "student": session["fullname"],
            "exam_title": selected_exam["title"],
            "subject": selected_exam["subject"],
            "score": score,
            "school": session["school"]
        }

        results.append(result)

        save_json(RESULTS_FILE, results)

        return render_template(
            "exam_result.html",
            score=score,
            exam=selected_exam
        )

    return render_template(
        "take_exam.html",
        exam=selected_exam
    )


# =========================================
# RESULTS
# =========================================
@app.route("/results")
def results():

    if "user" not in session:
        return redirect(url_for("login"))

    results = load_json(RESULTS_FILE)

    student_results = []

    for result in results:

        if result["student"] == session["fullname"]:
            student_results.append(result)

    return render_template(
        "results.html",
        results=student_results
    )


# =========================================
# FILE UPLOAD SYSTEM
# =========================================
@app.route("/upload-file", methods=["GET", "POST"])
def upload_file():

    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        uploaded_file = request.files["file"]

        if uploaded_file.filename != "":

            filename = secure_filename(uploaded_file.filename)

            uploaded_file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            flash("File uploaded successfully!", "success")

            return redirect(url_for("upload_file"))

    return render_template("upload_file.html")


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
