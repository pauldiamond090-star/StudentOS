from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="StudentOS")


# =========================================================
# MODELS
# =========================================================

class Student(BaseModel):
    name: str
    age: int
    class_name: str


students = []


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to StudentOS",
        "status": "running",
        "platform": "AI Powered School System"
    }


# =========================================================
# STUDENT MANAGEMENT
# =========================================================

@app.post("/students/add")
def add_student(student: Student):
    students.append(student.dict())

    return {
        "message": "Student added successfully",
        "student": student
    }


@app.get("/students")
def get_students():
    return students


# =========================================================
# NURSERY CLASSES
# =========================================================

@app.get("/nursery")
def nursery():
    return {
        "classes": {
            "Nursery 1": [
                "Alphabet",
                "Numbers",
                "Rhymes",
                "Drawing",
                "Coloring",
                "Storytelling",
                "Health Habits",
                "Writing Practice"
            ],

            "Nursery 2": [
                "English",
                "Mathematics",
                "Rhymes",
                "Basic Science",
                "Drawing",
                "Handwriting",
                "Moral Instruction",
                "Physical Education"
            ]
        }
    }


# =========================================================
# PRIMARY CLASSES
# =========================================================

@app.get("/primary")
def primary():
    return {
        "classes": {

            "Primary 1": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Social Studies",
                "Civic Education",
                "Computer Studies",
                "Cultural and Creative Arts",
                "Physical and Health Education",
                "Agricultural Science"
            ],

            "Primary 2": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Social Studies",
                "Civic Education",
                "Computer Studies",
                "Verbal Reasoning",
                "Quantitative Reasoning",
                "Agricultural Science"
            ],

            "Primary 3": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Social Studies",
                "Computer Studies",
                "Civic Education",
                "Cultural and Creative Arts",
                "Home Economics",
                "Agricultural Science"
            ],

            "Primary 4": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Social Studies",
                "Computer Science",
                "French",
                "Civic Education",
                "Agricultural Science",
                "Home Economics"
            ],

            "Primary 5": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Social Studies",
                "Computer Science",
                "French",
                "Agricultural Science",
                "Verbal Reasoning",
                "Quantitative Reasoning"
            ],

            "Primary 6": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Social Studies",
                "Computer Science",
                "Civic Education",
                "French",
                "Agricultural Science",
                "Home Economics"
            ]
        }
    }


# =========================================================
# JUNIOR SECONDARY SCHOOL
# =========================================================

@app.get("/junior-secondary")
def junior_secondary():
    return {
        "classes": {

            "JSS1": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Basic Technology",
                "Social Studies",
                "Computer Science",
                "Business Studies",
                "Civic Education",
                "Agricultural Science",
                "Cultural and Creative Arts",
                "French",
                "Home Economics"
            ],

            "JSS2": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Basic Technology",
                "Social Studies",
                "Computer Science",
                "Business Studies",
                "Civic Education",
                "Agricultural Science",
                "French",
                "Home Economics",
                "Security Education"
            ],

            "JSS3": [
                "English Language",
                "Mathematics",
                "Basic Science",
                "Basic Technology",
                "Social Studies",
                "Computer Science",
                "Business Studies",
                "Civic Education",
                "Agricultural Science",
                "French",
                "Home Economics",
                "Cultural and Creative Arts"
            ]
        }
    }


# =========================================================
# SENIOR SECONDARY SCHOOL
# =========================================================

@app.get("/senior-secondary")
def senior_secondary():
    return {
        "classes": {

            "SS1 Science": [
                "English Language",
                "Mathematics",
                "Physics",
                "Chemistry",
                "Biology",
                "Computer Science",
                "Further Mathematics",
                "Agricultural Science",
                "Civic Education"
            ],

            "SS2 Science": [
                "English Language",
                "Mathematics",
                "Physics",
                "Chemistry",
                "Biology",
                "Computer Science",
                "Further Mathematics",
                "Technical Drawing",
                "Civic Education"
            ],

            "SS3 Science": [
                "English Language",
                "Mathematics",
                "Physics",
                "Chemistry",
                "Biology",
                "Computer Science",
                "Further Mathematics",
                "Agricultural Science",
                "Civic Education"
            ],

            "SS1 Commercial": [
                "English Language",
                "Mathematics",
                "Economics",
                "Commerce",
                "Accounting",
                "Marketing",
                "Computer Science",
                "Civic Education"
            ],

            "SS2 Commercial": [
                "English Language",
                "Mathematics",
                "Economics",
                "Commerce",
                "Accounting",
                "Office Practice",
                "Computer Science",
                "Civic Education"
            ],

            "SS3 Commercial": [
                "English Language",
                "Mathematics",
                "Economics",
                "Commerce",
                "Accounting",
                "Marketing",
                "Computer Science",
                "Civic Education"
            ],

            "SS1 Art": [
                "English Language",
                "Mathematics",
                "Government",
                "Literature",
                "Christian Religious Studies",
                "Civic Education",
                "Fine Arts",
                "Computer Science"
            ],

            "SS2 Art": [
                "English Language",
                "Mathematics",
                "Government",
                "Literature",
                "Christian Religious Studies",
                "Civic Education",
                "History",
                "Computer Science"
            ],

            "SS3 Art": [
                "English Language",
                "Mathematics",
                "Government",
                "Literature",
                "Christian Religious Studies",
                "Civic Education",
                "History",
                "Computer Science"
            ]
        }
    }


# =========================================================
# RESULTS
# =========================================================

@app.get("/results")
def results():
    return {
        "results": [
            {
                "name": "Paul",
                "class": "SS2 Science",
                "average": 89
            },
            {
                "name": "Grace",
                "class": "Primary 5",
                "average": 92
            }
        ]
    }


# =========================================================
# TIMETABLE
# =========================================================

@app.get("/timetable")
def timetable():
    return {
        "Monday": [
            "English",
            "Mathematics",
            "Physics",
            "Chemistry"
        ],

        "Tuesday": [
            "Biology",
            "Computer Science",
            "Economics",
            "Civic Education"
        ]
    }


# =========================================================
# TEACHERS
# =========================================================

@app.get("/teachers")
def teachers():
    return {
        "teachers": [
            {
                "name": "Mr John",
                "subject": "Mathematics"
            },

            {
                "name": "Mrs Grace",
                "subject": "English Language"
            }
        ]
    }
