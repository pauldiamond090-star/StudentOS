from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="StudentOS")

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
@app.post("/register", response_class=HTMLResponse)
def register(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    return f"""
    <h1>Account Created Successfully</h1>

    <p>Username: {username}</p>

    <p>Role: {role}</p>

    <a href="/">Go To Login</a>
    """

# LOGIN USER
@app.post("/login", response_class=HTMLResponse)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return f"""
    <h1>Login Successful</h1>

    <p>Welcome {username}</p>
    """
