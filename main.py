from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
import json, os, uuid

app = Flask(__name__)
app.secret_key = "super_saas_secret_2026"

# =========================
# OAUTH GOOGLE
# =========================
oauth = OAuth(app)

app.config["GOOGLE_CLIENT_ID"] = "YOUR_CLIENT_ID"
app.config["GOOGLE_CLIENT_SECRET"] = "YOUR_CLIENT_SECRET"

google = oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "email profile"},
)

# =========================
# DATA FILES
# =========================
DATA = "data"
os.makedirs(DATA, exist_ok=True)

USERS_FILE = f"{DATA}/users.json"
SCHOOLS_FILE = f"{DATA}/schools.json"
HOMEWORK_FILE = f"{DATA}/homework.json"
CBT_FILE = f"{DATA}/cbt.json"
CHAT_FILE = f"{DATA}/chat.json"

for f in [USERS_FILE, SCHOOLS_FILE, HOMEWORK_FILE, CBT_FILE, CHAT_FILE]:
    if not os.path.exists(f):
        with open(f, "w") as x:
            json.dump([], x)

# =========================
# HELPERS
# =========================
def load(file):
    with open(file) as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def current_school():
    return session.get("school_id")

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return redirect(url_for("login"))

# =========================
# REGISTER SCHOOL (MULTI-SCHOOL)
# =========================
@app.route("/create-school", methods=["POST"])
def create_school():

    schools = load(SCHOOLS_FILE)

    school = {
        "id": str(uuid.uuid4()),
        "name": request.form.get("school_name"),
        "owner": request.form.get("email")
    }

    schools.append(school)
    save(SCHOOLS_FILE, schools)

    return "School created"

# =========================
# REGISTER USER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    users = load(USERS_FILE)

    if request.method == "POST":

        user = {
            "id": str(uuid.uuid4()),
            "fullname": request.form["fullname"],
            "email": request.form["email"],
            "password": generate_password_hash(request.form["password"]),
            "role": request.form["role"],
            "school_id": request.form.get("school_id")
        }

        users.append(user)
        save(USERS_FILE, users)

        return redirect("/login")

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

                return redirect("/dashboard")

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
            return redirect("/dashboard")

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

    return redirect("/dashboard")

# =========================
# DASHBOARD ROUTER
# =========================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    if session["role"] == "admin":
        return render_template("admin.html")

    if session["role"] == "teacher":
        return render_template("teacher.html")

    return render_template("student.html")

# =========================
# HOMEWORK SYSTEM
# =========================
@app.route("/homework", methods=["GET", "POST"])
def homework():

    data = load(HOMEWORK_FILE)

    if request.method == "POST":

        hw = {
            "id": str(uuid.uuid4()),
            "school_id": session["school_id"],
            "title": request.form["title"],
            "body": request.form["body"],
            "teacher": session["user"]
        }

        data.append(hw)
        save(HOMEWORK_FILE, data)

    return {"homework": data}

# =========================
# CBT SYSTEM (BASIC)
# =========================
@app.route("/cbt", methods=["GET", "POST"])
def cbt():

    data = load(CBT_FILE)

    if request.method == "POST":

        exam = {
            "id": str(uuid.uuid4()),
            "school_id": session["school_id"],
            "question": request.form["question"],
            "answer": request.form["answer"]
        }

        data.append(exam)
        save(CBT_FILE, data)

    return {"cbt": data}

# =========================
# CHAT SYSTEM (BASIC)
# =========================
@app.route("/chat", methods=["POST"])
def chat():

    data = load(CHAT_FILE)

    msg = {
        "user": session["user"],
        "message": request.form["message"],
        "school_id": session["school_id"]
    }

    data.append(msg)
    save(CHAT_FILE, data)

    return {"status": "sent"}

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
