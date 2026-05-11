from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="StudentOS")


# =========================================================
# TEMP DATABASE
# =========================================================

users = []


# =========================================================
# MODELS
# =========================================================

class User(BaseModel):
    username: str
    password: str
    role: str


class LoginData(BaseModel):
    username: str
    password: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to StudentOS",
        "status": "running",
        "platform": "Multi User AI School Platform"
    }


# =========================================================
# REGISTER
# =========================================================

@app.post("/register")
def register(user: User):

    for existing_user in users:
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

    users.append(user.dict())

    return {
        "message": "User registered successfully",
        "user": user
    }


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login(data: LoginData):

    for user in users:
        if (
            user["username"] == data.username
            and user["password"] == data.password
        ):
            return {
                "message": "Login successful",
                "role": user["role"]
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid username or password"
    )


# =========================================================
# USERS
# =========================================================

@app.get("/users")
def get_users():
    return users


# =========================================================
# NURSERY
# =========================================================

@app.get("/nursery")
def nursery():
    return {
        "Nursery 1": [
            "Alphabet",
            "Numbers",
            "Rhymes",
            "Drawing",
            "Coloring"
        ],

        "Nursery 2": [
            "English",
            "Mathematics",
            "Basic Science",
            "Writing",
            "Health Habits"
        ]
    }


# =========================================================
# PRIMARY
# =========================================================

@app.get("/primary")
def primary():
    return {
        "Primary 1": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "Social Studies",
            "Computer Studies"
        ],

        "Primary 2": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "Social Studies",
            "Agricultural Science"
        ],

        "Primary 3": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "Computer Science",
            "Home Economics"
        ],

        "Primary 4": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "French",
            "Computer Science"
        ],

        "Primary 5": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "Agricultural Science",
            "Computer Science"
        ],

        "Primary 6": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "Computer Science",
            "Civic Education"
        ]
    }


# =========================================================
# JUNIOR SECONDARY
# =========================================================

@app.get("/junior-secondary")
def junior_secondary():
    return {
        "JSS1": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "Basic Technology",
            "Computer Science",
            "Business Studies"
        ],

        "JSS2": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "Agricultural Science",
            "Computer Science",
            "French"
        ],

        "JSS3": [
            "English Language",
            "Mathematics",
            "Basic Science",
            "Computer Science",
            "Business Studies",
            "Civic Education"
        ]
    }


# =========================================================
# SENIOR SECONDARY
# =========================================================

@app.get("/senior-secondary")
def senior_secondary():
    return {
        "Science": [
            "Physics",
            "Chemistry",
            "Biology",
            "Further Mathematics",
            "Computer Science"
        ],

        "Commercial": [
            "Economics",
            "Commerce",
            "Accounting",
            "Marketing",
            "Office Practice"
        ],

        "Arts": [
            "Government",
            "Literature",
            "History",
            "CRS",
            "Fine Arts"
        ]
    }


# =========================================================
# UNIVERSITY / INSTITUTIONS
# =========================================================

@app.get("/institutions")
def institutions():
    return {
        "Engineering": [
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering",
            "Computer Engineering"
        ],

        "Medical Sciences": [
            "Medicine",
            "Nursing",
            "Pharmacy",
            "Anatomy"
        ],

        "Sciences": [
            "Computer Science",
            "Physics",
            "Chemistry",
            "Biochemistry",
            "Mathematics"
        ],

        "Management Sciences": [
            "Accounting",
            "Business Administration",
            "Marketing",
            "Banking and Finance"
        ],

        "Arts and Humanities": [
            "English",
            "History",
            "Philosophy",
            "Linguistics"
        ]
    }


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/dashboard")
def dashboard():
    return {
        "features": [
            "Student Login",
            "Teacher Login",
            "Admin Login",
            "Homework Upload",
            "AI Tutor",
            "Timetable",
            "Exam Practice",
            "Results",
            "Subjects",
            "Assignments",
            "Study Planner"
        ]
}
