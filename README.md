from flask import Flask, request, redirect, url_for, render_template_string, Response, jsonify
import sqlite3
import wolframalpha
import pytesseract
from PIL import Image
import speech_recognition as sr
from gtts import gTTS
import os

from flask_login import (
    LoginManager, UserMixin,
    login_user, logout_user,
    login_required, current_user
)

from werkzeug.security import generate_password_hash, check_password_hash


# ==========================================================
# Flask Setup
# ==========================================================
app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager(app)
login_manager.login_view = "login"


# ==========================================================
# Database Setup
# ==========================================================
db = sqlite3.connect("homework_hero.db", check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Create Questions Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    question TEXT,
    answer TEXT
)
""")

db.commit()


# ==========================================================
# WolframAlpha Setup
# ==========================================================
# Your App ID inserted here
wolfram_client = wolframalpha.Client("4L7WHVJV6A")


# ==========================================================
# User Model
# ==========================================================
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        return User(user["id"], user["username"])
    return None


# ==========================================================
# HTML Templates (All Inside Python)
# ==========================================================

INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Homework Hero</title>
  <link rel="stylesheet"
        href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
</head>

<body class="container mt-5">

<h1>📚 Homework Hero</h1>

<p>Hi, <b>{{ current_user.username }}</b> |
<a href="/logout">Logout</a></p>

<form action="/ask" method="post" enctype="multipart/form-data">

  <input type="text" name="text"
         placeholder="Type your question here..."
         class="form-control mb-2">

  <input type="file" name="voice"
         accept=".wav"
         class="form-control mb-2">

  <input type="file" name="image"
         accept="image/*"
         class="form-control mb-2">

  <button class="btn btn-primary">Ask Question</button>
</form>

<hr>

{% if answer %}
<h3>✅ Answer:</h3>
<p>{{ answer }}</p>

<button class="btn btn-success"
onclick="readAloud({{ answer|tojson }})">
🔊 Read Aloud</button>
{% endif %}

{% if error %}
<p style="color:red;">❌ Error: {{ error }}</p>
{% endif %}

<hr>

<h2>📌 History</h2>

{% for q in history %}
<p>
<b>{{ q["question"] }}</b> → {{ q["answer"] }}

<form action="/delete/{{ q['id'] }}" method="post" style="display:inline;">
  <button class="btn btn-sm btn-danger">Delete</button>
</form>
</p>
{% endfor %}

<form action="/clear" method="post">
  <button class="btn btn-danger">Clear History</button>
</form>

<form action="/export" method="post">
  <button class="btn btn-info mt-2">Export History CSV</button>
</form>

<script>
function readAloud(text){
  fetch("/speak",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({text:text})
  });
  alert("Speech saved as static/speech.mp3");
}
</script>

</body>
</html>
"""


LOGIN_HTML = """
<h2>Login</h2>

<form method="post">
  <input name="username" placeholder="Username"><br><br>
  <input name="password" type="password" placeholder="Password"><br><br>
  <button>Login</button>
</form>

<a href="/register">Register</a>
"""


REGISTER_HTML = """
<h2>Register</h2>

<form method="post">
  <input name="username" placeholder="Username"><br><br>
  <input name="password" type="password" placeholder="Password"><br><br>
  <button>Register</button>
</form>

<a href="/login">Login</a>
"""


# ==========================================================
# Routes
# ==========================================================

# Home Page
@app.route("/")
@login_required
def index():
    cursor.execute("SELECT * FROM questions WHERE user_id=?", (current_user.id,))
    history = cursor.fetchall()
    return render_template_string(INDEX_HTML, history=history, answer=None, error=None)


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        try:
            cursor.execute("INSERT INTO users (username,password) VALUES (?,?)",
                           (username, password))
            db.commit()
            return redirect("/login")
        except:
            return "Username already exists!"

    return render_template_string(REGISTER_HTML)


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            login_user(User(user["id"], user["username"]))
            return redirect("/")

        return "Invalid Login!"

    return render_template_string(LOGIN_HTML)


# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# Ask Question
@app.route("/ask", methods=["POST"])
@login_required
def ask():
    try:
        question_text = request.form.get("text")

        # Image OCR
        if "image" in request.files and request.files["image"].filename != "":
            img = Image.open(request.files["image"])
            question_text = pytesseract.image_to_string(img)

        # Voice Recognition
        if "voice" in request.files and request.files["voice"].filename != "":
            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(request.files["voice"])
            with audio_file as source:
                audio = recognizer.record(source)
            question_text = recognizer.recognize_google(audio)

        if not question_text:
            return redirect("/")

        # WolframAlpha Answer
        res = wolfram_client.query(question_text)
        answer_text = next(res.results).text

        # Save to Database
        cursor.execute(
            "INSERT INTO questions (user_id, question, answer) VALUES (?,?,?)",
            (current_user.id, question_text, answer_text)
        )
        db.commit()

        cursor.execute("SELECT * FROM questions WHERE user_id=?", (current_user.id,))
        history = cursor.fetchall()

        return render_template_string(INDEX_HTML, history=history,
                                      answer=answer_text, error=None)

    except Exception as e:
        cursor.execute("SELECT * FROM questions WHERE user_id=?", (current_user.id,))
        history = cursor.fetchall()

        return render_template_string(INDEX_HTML, history=history,
                                      answer=None, error=str(e))


# Delete One Question
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    cursor.execute("DELETE FROM questions WHERE id=? AND user_id=?",
                   (id, current_user.id))
    db.commit()
    return redirect("/")


# Clear All History
@app.route("/clear", methods=["POST"])
@login_required
def clear():
    cursor.execute("DELETE FROM questions WHERE user_id=?", (current_user.id,))
    db.commit()
    return redirect("/")


# Export History CSV
@app.route("/export", methods=["POST"])
@login_required
def export():
    cursor.execute("SELECT question, answer FROM questions WHERE user_id=?",
                   (current_user.id,))
    rows = cursor.fetchall()

    output = "Question,Answer\n"
    for row in rows:
        output += f"{row['question']},{row['answer']}\n"

    return Response(output,
                    mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=history.csv"})


# Speak Answer
@app.route("/speak", methods=["POST"])
@login_required
def speak():
    data = request.get_json()
    text = data["text"]

    if not os.path.exists("static"):
        os.mkdir("static")

    tts = gTTS(text)
    tts.save("static/speech.mp3")

    return jsonify({"status": "ok"})


# ==========================================================
# Run App
# ==========================================================
if __name__ == "__main__":
    app.run(debug=True) shiny-octo-system
