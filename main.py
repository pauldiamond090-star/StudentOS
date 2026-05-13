from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, User
from auth import hash_password, verify_password

app = FastAPI(title="StudentOS")

# Create database tables
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

# REGISTER PAGE
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

# REGISTER USER
@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...)
):
    db: Session = SessionLocal()

    existing_user = db.query(User).filter(
        User.username == username
    ).first()

    if existing_user:
        return {"message": "Username already exists"}

    new_user = User(
        username=username,
        password=hash_password(password),
        role=role
    )

    db.add(new_user)
    db.commit()

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
    db: Session = SessionLocal()

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        return {"message": "User not found"}

    if not verify_password(password, user.password):
        return {"message": "Incorrect password"}

    # REDIRECT BASED ON ROLE
    if user.role == "teacher":
        return RedirectResponse(
            url=f"/teacher/{user.username}",
            status_code=303
        )

    elif user.role == "admin":
        return RedirectResponse(
            url=f"/admin/{user.username}",
            status_code=303
        )

    else:
        return RedirectResponse(
            url=f"/student/{user.username}",
            status_code=303
        )

# STUDENT DASHBOARD
@app.get("/student/{username}", response_class=HTMLResponse)
def student_dashboard(username: str, request: Request):
    return templates.TemplateResponse(
        "Student_dashboard.html",
        {
            "request": request,
            "username": username
        }
    )

# TEACHER DASHBOARD
@app.get("/teacher/{username}", response_class=HTMLResponse)
def teacher_dashboard(username: str, request: Request):
    return templates.TemplateResponse(
        "teacher_dashboard.html",
        {
            "request": request,
            "username": username
        }
    )

# ADMIN DASHBOARD
@app.get("/admin/{username}", response_class=HTMLResponse)
def admin_dashboard(username: str, request: Request):
    return HTMLResponse(f"""
    <h1>Admin Dashboard</h1>
    <h2>Welcome {username}</h2>
    """)
