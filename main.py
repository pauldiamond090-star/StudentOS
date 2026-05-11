
from fastapi import FastAPI

app = FastAPI(title="StudentOS")


@app.get("/")
def home():
    return {
        "message": "Welcome to StudentOS",
        "description": "AI Student Operating System"
    }


# =====================================================
# NURSERY SUBJECTS
# =====================================================

@app.get("/nursery")
def nursery_subjects():
    return {
        "level": "Nursery",
        "subjects": [
            "Alphabet",
            "Numbers",
            "Colors",
            "Shapes",
            "Rhymes",
            "Drawing",
            "Speaking Practice",
            "Story Time"
        ]
    }


# =====================================================
# PRIMARY SCHOOL SUBJECTS
# =====================================================

@app.get("/primary")
def primary_subjects():
    return {
        "level": "Primary School",
        "subjects": [
            "Mathematics",
            "English Language",
            "Basic Science",
            "Social Studies",
            "Civic Education",
            "Computer Studies",
            "Agricultural Science",
            "Home Economics",
            "Physical and Health Education",
            "Verbal Reasoning",
            "Quantitative Reasoning"
        ]
    }


# =====================================================
# SECONDARY SCHOOL SUBJECTS
# =====================================================

@app.get("/secondary")
def secondary_subjects():
    return {
        "level": "Secondary School",
        "subjects": [
            "Mathematics",
            "English Language",
            "Physics",
            "Chemistry",
            "Biology",
            "Further Mathematics",
            "Economics",
            "Government",
            "Literature",
            "Commerce",
            "Accounting",
            "CRS",
            "IRS",
            "Geography",
            "Agricultural Science",
            "Computer Science",
            "Technical Drawing",
            "Food and Nutrition",
            "French",
            "Yoruba",
            "Igbo",
            "Hausa"
        ]
    }


# =====================================================
# UNIVERSITY FACULTIES
# =====================================================

@app.get("/university")
def university():
    return {
        "level": "University",
        "faculties": {
            "Engineering": [
                "Mechanical Engineering",
                "Civil Engineering",
                "Electrical Engineering",
                "Computer Engineering"
            ],

            "Sciences": [
                "Computer Science",
                "Microbiology",
                "Biochemistry",
                "Physics",
                "Chemistry",
                "Mathematics"
            ],

            "Medical Sciences": [
                "Medicine",
                "Nursing",
                "Pharmacy",
                "Anatomy"
            ],

            "Arts": [
                "English",
                "History",
                "Linguistics",
                "Philosophy"
            ],

            "Social Sciences": [
                "Economics",
                "Political Science",
                "Psychology",
                "Sociology"
            ],

            "Management Sciences": [
                "Accounting",
                "Business Administration",
                "Marketing",
                "Banking and Finance"
            ]
        }
    }


# =====================================================
# EXAMS
# =====================================================

@app.get("/exams")
def exams():
    return {
        "supported_exams": [
            "JAMB",
            "WAEC",
            "NECO",
            "GCE",
            "BECE",
            "SAT",
            "IELTS",
            "TOEFL",
            "University Post-UTME"
        ]
    }


# =====================================================
# AI FEATURES
# =====================================================

@app.get("/features")
def features():
    return {
        "features": [
            "AI Tutor",
            "Homework Scanner",
            "OCR Text Extraction",
            "Exam Practice",
            "Saved Notes",
            "Flashcards",
            "Study Planner",
            "Timetable",
            "Voice Learning",
            "Offline Learning",
            "Career Guidance",
            "Scholarship Alerts",
            "Study Groups",
            "CBT Practice"
        ]
    }


# =====================================================
# STUDENT TOOLS
# =====================================================

@app.get("/tools")
def tools():
    return {
        "student_tools": [
            "Scientific Calculator",
            "GPA Calculator",
            "PDF Reader",
            "Voice Recorder",
            "Study Timer",
            "Whiteboard",
            "Unit Converter",
            "Citation Generator"
        ]
    }
