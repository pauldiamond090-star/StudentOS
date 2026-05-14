from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)

# ==========================================
# SECRET KEY
# ==========================================
app.secret_key = "nexora_ultra_secure_key_2026"

# ==========================================
# DATABASE FILE
# ==========================================
USERS_FILE = "users.json"

# ==========================================
# LOAD USERS
# ==========================================
def load_users():

    if not os.path.exists(USERS_FILE):

        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

    with open(USERS_FILE, "r") as f:

        try:
            data = json.load(f)

            if isinstance(data, list):
                return {}

            return data

        except:
            return {}


# ==========================================
# SAVE USERS
# ==========================================
def save_users(users):

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# ==========================================
# SPLASH SCREEN
# ==========================================
@app.route("/")
def splash():

    return render_template("splash.html")


# ==========================================
# LOGIN
# ==========================================
@app.route("/login", methods=["GET", "POST"])
def login():

    users = load_users()

    if request.method == "POST":

        username = request.form["username"].strip().lower()
        password = request.form["password"]

        if username in users:

            stored_password = users[username]["password"]

            if check_password_hash(stored_password, password):

                session["user"] = username
                session["role"] = users[username]["role"]

                flash("Welcome to Nexora!", "success")

                # STUDENT
                if users[username]["role"] == "student":

                    return redirect(
                        url_for("student_dashboard")
                    )

                # TEACHER
                elif users[username]["role"] == "teacher":

                    return redirect(
                        url_for("teacher_dashboard")
                    )

                # ADMIN
                elif users[username]["role"] == "admin":

                    return redirect(
                        url_for("admin_dashboard")
                    )

        flash("Invalid username or password", "error")

    return render_template("login.html")


# ==========================================
# REGISTER
# ==========================================
@app.route("/register", methods=["GET", "POST"])
def register():

    users = load_users()

    if request.method == "POST":

        username = request.form["username"].strip().lower()
        password = request.form["password"]
        role = request.form["role"]

        # CHECK USER EXISTS
        if username in users:

            flash("User already exists!", "error")

            return redirect(
                url_for("register")
            )

        # PASSWORD VALIDATION
        if len(password) < 6:

            flash(
                "Password must be at least 6 characters",
                "error"
            )

            return redirect(
                url_for("register")
            )

        # SAVE USER
        users[username] = {
            "password": generate_password_hash(password),
            "role": role
        }

        save_users(users)

        flash(
            "Account created successfully!",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template("register.html")


# ==========================================
# STUDENT DASHBOARD
# ==========================================
@app.route("/student/dashboard")
def student_dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] != "student":

        return redirect(
            url_for("login")
        )

    return render_template(
        "student_dashboard.html",
        user=session["user"]
    )


# ==========================================
# TEACHER DASHBOARD
# ==========================================
@app.route("/teacher/dashboard")
def teacher_dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] != "teacher":

        return redirect(
            url_for("login")
        )

    return render_template(
        "teacher_dashboard.html",
        user=session["user"]
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================
@app.route("/admin/dashboard")
def admin_dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    if session["role"] != "admin":

        return redirect(
            url_for("login")
        )

    return render_template(
        "admin_dashboard.html",
        user=session["user"]
    )


# ==========================================
# HOMEWORK PAGE
# ==========================================
@app.route("/homework")
def homework():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "homework.html"
    )


# ==========================================
# TIMETABLE PAGE
# ==========================================
@app.route("/timetable")
def timetable():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "timetable.html"
    )


# ==========================================
# CHAT PAGE
# ==========================================
@app.route("/chat")
def chat():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "chat.html"
    )


# ==========================================
# LOGOUT
# ==========================================
@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
