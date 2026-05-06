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

<form action="/delete/{{ q['id']
