from flask import Flask, render_template_string, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "studentos_secret_key"


# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect("studentos.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# SPLASH SCREEN
# =========================

@app.route("/")
def splash():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>StudentOS</title>

        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {
                margin: 0;
                font-family: Arial;
                background: linear-gradient(to bottom, #d50000, #ff3d00, #8e0000);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                overflow: hidden;
            }

            .container {
                text-align: center;
            }

            .logo {
                font-size: 60px;
                font-weight: bold;
            }

            .version {
                margin-top: 20px;
                font-size: 22px;
            }
        </style>

        <script>
            setTimeout(function(){
                window.location.href='/welcome';
            }, 60000);
        </script>
    </head>

    <body>
        <div class="container">
            <div class="logo">StudentOS</div>
            <div class="version">v8.1.0</div>
        </div>
    </body>
    </html>
    """)


# =========================
# WELCOME SCREEN
# =========================

@app.route("/welcome")
def welcome():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {
                margin:0;
                font-family:Arial;
                background:#fff4ef;
                padding:30px;
                text-align:center;
            }

            h1 {
                color:#c40000;
                font-size:45px;
            }

            .image {
                width:100%;
                height:300px;
                border-radius:30px;
                background:#eee;
                margin-top:40px;
            }

            .title {
                font-size:45px;
                font-weight:bold;
                margin-top:40px;
            }

            .btn {
                display:block;
                width:100%;
                padding:20px;
                border-radius:50px;
                border:none;
                font-size:22px;
                margin-top:20px;
                text-decoration:none;
            }

            .login {
                background:white;
                border:2px solid #ddd;
                color:#c40000;
            }

            .create {
                background:#c40000;
                color:white;
            }

            .guest {
                color:#c40000;
                margin-top:30px;
                display:block;
                font-size:22px;
                text-decoration:none;
            }
        </style>
    </head>

    <body>
        <h1>StudentOS</h1>

        <div class="image"></div>

        <div class="title">
            Study and practice for any CBT
        </div>

        <a href="/login" class="btn login">Login</a>

        <a href="/register" class="btn create">Create Account</a>

        <a href="/dashboard" class="guest">Continue as Guest</a>
    </body>
    </html>
    """)


# =========================
# REGISTER
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    message = ""

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            conn = sqlite3.connect('studentos.db', timeout=10)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",
                (fullname, email, password)
            )

            conn.commit()
            conn.close()

            return redirect('/login')

        except sqlite3.IntegrityError:
            message = "Email already exists"

    return render_template_string("""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {
                font-family:Arial;
                padding:30px;
            }

            input {
                width:100%;
                padding:18px;
                margin-top:15px;
                border-radius:20px;
                border:2px solid #ddd;
                font-size:18px;
            }

            button {
                width:100%;
                padding:18px;
                margin-top:25px;
                background:#c40000;
                color:white;
                border:none;
                border-radius:50px;
                font-size:22px;
            }
        </style>
    </head>

    <body>
        <h1>Create Account</h1>

        <p style='color:red;'>{{message}}</p>

        <form method="POST">
            <input type="text" name="fullname" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>

            <button>Create Account</button>
        </form>
    </body>
    </html>
    """, message=message)


# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    message = ""

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('studentos.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[3], password):
            session['user'] = user[1]
            return redirect('/dashboard')

        else:
            message = "Invalid login"

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {
                font-family:Arial;
                padding:30px;
                background:white;
            }

            .google {
                width:100%;
                padding:20px;
                border:2px solid #ddd;
                border-radius:25px;
                text-align:center;
                font-size:22px;
                margin-top:30px;
            }

            input {
                width:100%;
                padding:20px;
                margin-top:20px;
                border-radius:20px;
                border:2px solid #ddd;
                font-size:20px;
            }

            button {
                width:100%;
                padding:20px;
                margin-top:30px;
                border:none;
                border-radius:50px;
                background:#c40000;
                color:white;
                font-size:22px;
            }
        </style>
    </head>

    <body>
        <h1 style="font-size:50px;">Welcome Back</h1>

        <div class="google">
            Continue with Google
        </div>

        <center>
            <h2>OR</h2>
        </center>

        <p style='color:red;'>{{message}}</p>

        <form method="POST">
            <input type="email" name="email" placeholder="Username or Email" required>

            <input type="password" name="password" placeholder="Enter Password" required>

            <button>Login</button>
        </form>
    </body>
    </html>
    """, message=message)


# =========================
# DASHBOARD
# =========================

@app.route('/dashboard')
def dashboard():

    username = session.get('user', 'Prince')

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>
            body {
                font-family:Arial;
                padding:25px;
                background:#fafafa;
            }

            .card {
                background:white;
                border-radius:25px;
                padding:25px;
                margin-top:20px;
                box-shadow:0 2px 10px rgba(0,0,0,0.05);
            }

            .green {
                background:#e9f7e9;
            }

            .blue {
                background:#eaf4ff;
            }

            .orange {
                background:#fff2e5;
            }

            .grid {
                display:grid;
                grid-template-columns:1fr 1fr;
                gap:15px;
                margin-top:20px;
            }

            .small {
                height:150px;
            }
        </style>
    </head>

    <body>

        <h1>Hello, {{username}}</h1>

        <div class="card orange">
            <h2>CBT Simulator</h2>
            <p>Practice for any CBT exam online.</p>
        </div>

        <div class="card green">
            <h2>JAMB CBT Simulator</h2>
            <p>Practice JAMB UTME past questions.</p>
        </div>

        <div class="card blue">
            <h2>WAEC CBT Simulator</h2>
            <p>Practice WAEC past questions.</p>
        </div>

        <h2 style="margin-top:40px;">Quick Links</h2>

        <div class="grid">

            <div class="card small">
                <h3>Study Past Questions</h3>
            </div>

            <div class="card small">
                <h3>StudentOS Store</h3>
            </div>

            <div class="card small">
                <h3>Video Lessons</h3>
            </div>

            <div class="card small">
                <h3>Novels</h3>
            </div>

        </div>

    </body>
    </html>
    """, username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
