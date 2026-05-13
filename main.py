from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import os

app = FastAPI(title="StudentOS")

USERS_FILE = "users.json"

# CREATE FILE IF MISSING
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

# LOAD USERS
def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# SAVE USERS
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# LOGIN PAGE
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>StudentOS Login</title>
    </head>
    <body>

    <h1>StudentOS Login</h1>

    <form action="/login" method="post">

        <input type="text"
               name="username"
               placeholder="Username"
               required>

        <br><br>

        <input type="password"
               name="password"
               placeholder="Password"
               required>

        <br><br>

        <button type="submit">
            Login
        </button>

    </form>

    <br>

    <a href="/register">
        Create Account
    </a>

    </body>
    </html>
    """

# REGISTER PAGE
@app.get("/register", response_class=HTMLResponse)
def register_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register</title>
    </head>
    <body>

    <h1>Create Account</h1>

    <form action="/register" method="post">

        <input type="text"
               name="username"
               placeholder="Username"
               required>

        <br><br>

        <input type="password"
               name="password"
               placeholder="Password"
               required>

        <br><br>

        <select name="role">
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
            <option value="admin">Admin</option>
        </select>

        <br><br>

        <button type="submit">
            Register
        </button>

    </form>

    </body>
    </html>
    """

# REGISTER USER
@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    users = load_users()

    # CHECK IF USER EXISTS
    for user in users:
        if user["username"] == username:
            return HTMLResponse("""
            <h1>Username already exists</h1>
            <a href="/register">Try Again</a>
            """)

    # SAVE USER
    users.append({
        "username": username,
        "password": password,
        "role": role
    })

    save_users(users)

    return RedirectResponse(
        url="/",
        status_code=303
    )

# LOGIN USER
@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    users = load_users()

    for user in users:

        if (
            user["username"] == username
            and
            user["password"] == password
        ):

            # REDIRECT BY ROLE
            if user["role"] == "teacher":
                return RedirectResponse(
                    url=f"/teacher/{username}",
                    status_code=303
                )

            elif user["role"] == "admin":
                return RedirectResponse(
                    url=f"/admin/{username}",
                    status_code=303
                )

            else:
                return RedirectResponse(
                    url=f"/student/{username}",
                    status_code=303
                )

    return HTMLResponse("""
    <h1>Invalid username or password</h1>
    <a href="/">Try Again</a>
    """)

# STUDENT DASHBOARD
@app.get("/student/{username}", response_class=HTMLResponse)
def student_dashboard(username: str):
    return f"""
    <h1>Student Dashboard</h1>

    <p>Welcome {username}</p>
    """

# TEACHER DASHBOARD
@app.get("/teacher/{username}", response_class=HTMLResponse)
def teacher_dashboard(username: str):
    return f"""
    <h1>Teacher Dashboard</h1>

    <p>Welcome {username}</p>
    """

# ADMIN DASHBOARD
@app.get("/admin/{username}", response_class=HTMLResponse)
def admin_dashboard(username: str):
    return f"""
    <h1>Admin Dashboard</h1>

    <p>Welcome {username}</p>
    """
