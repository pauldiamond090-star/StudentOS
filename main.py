from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = "edunova_super_saas_2026"

# =========================
# DATA FOLDER
# =========================
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
SCHOOLS_FILE = os.path.join(DATA_FOLDER, "schools.json")
HOMEWORK_FILE = os.path.join(DATA_FOLDER, "homework.json")


# =========================
# INIT FILES
# =========================
def init_file(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=4)

init_file(USERS_FILE, [])
init_file(SCHOOLS_FILE, [])
init_file(HOMEWORK_FILE, [])


# =========================
# JSON HELPERS
# =========================
def load(file):
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return redirect(url_for("login"))


# =========================
# REGISTER USER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    users = load(USERS_FILE)

    if request.method == "POST":

        new_user = {
            "id": str(uuid.uuid4()),
            "fullname": request.form["fullname"],
            "email": request.form["email"],
            "password": generate_password_hash(request.form["password"]),
            "role": request.form["role"],
            "school_id": request.form.get("school_id")
        }

        users.append(new_user)
        save(USERS_FILE, users)

        flash("Account created!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    users = load(USERS_FILE)

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        for u in users:
            if u["email"] == email and check_password_hash(u["password"], password):

                session["user"] = u["email"]
                session["role"] = u["role"]
                session["school_id"] = u["school_id"]
                session["fullname"] = u["fullname"]

                return redirect(url_for("dashboard"))

        flash("Invalid login")

    return render_template("login.html")


# =========================
# GOOGLE LOGIN
# =========================
@app.route("/login/google")
def google_login():
    return google.authorize_redirect(url_for("google_callback", _external=True))


@app.route("/login/google/callback")
def google_callback():

    token = google.authorize_access_token()
    info = google.get("userinfo").json()

    users = load(USERS_FILE)

    for u in users:
        if u["email"] == info["email"]:

            session["user"] = u["email"]
            session["role"] = u["role"]
            session["school_id"] = u["school_id"]
            session["fullname"] = u["fullname"]

            return redirect(url_for("dashboard"))

    # auto create student
    new_user = {
        "id": str(uuid.uuid4()),
        "fullname": info["name"],
        "email": info["email"],
        "password": "",
        "role": "student",
        "school_id": None
    }

    users.append(new_user)
    save(USERS_FILE, users)

    session["user"] = new_user["email"]
    session["role"] = "student"
    session["school_id"] = None
    session["fullname"] = new_user["fullname"]

    return redirect(url_for("dashboard"))


# =========================
# MAIN DASHBOARD ROUTER
# =========================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    role = session.get("role")

    if role == "admin":
        return redirect(url_for("school_admin_dashboard"))

    if role == "teacher":
        return render_template("teacher_dashboard.html", user=session["fullname"])

    return render_template("student_dashboard.html", user=session["fullname"])


# =========================
# SCHOOL ADMIN DASHBOARD (MULTI-SCHOOL CORE)
# =========================
@app.route("/school-admin/dashboard")
def school_admin_dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    users = load(USERS_FILE)

    current = None

    for u in users:
        if u["email"] == session["user"]:
            current = u
            break

    if not current or current["role"] != "admin":
        flash("Access denied")
        return redirect(url_for("login"))

    school_id = current["school_id"]

    school_users = [u for u in users if u.get("school_id") == school_id]

    students = [u for u in school_users if u["role"] == "student"]
    teachers = [u for u in school_users if u["role"] == "teacher"]

    return render_template(
        "school_admin_dashboard.html",
        user=current,
        students=students,
        teachers=teachers,
        total_students=len(students),
        total_teachers=len(teachers)
    )


# =========================
# HOMEWORK SYSTEM
# =========================
@app.route("/homework")
def homework():

    data = load(HOMEWORK_FILE)

    return {"homework": data}


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
