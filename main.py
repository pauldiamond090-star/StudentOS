
from fastapi import FastAPI

app = FastAPI(title="StudentOS")


@app.get("/")
def home():
    return {
        "message": "Welcome to StudentOS",
        "status": "running"
    }


@app.get("/nursery")
def nursery():
    return {
        "level": "Nursery",
        "subjects": [
            "Alphabet",
            "Numbers",
            "Shapes",
            "Colors",
            "Drawing",
            "Rhymes"
        ]
    }


@app.get("/primary")
def primary():
    return {
        "level": "Primary School",
        "subjects": [
            "Mathematics",
            "English",
            "Basic Science",
            "Social Studies",
            "Computer Studies"
        ]
    }


@app.get("/secondary")
def secondary():
    return {
        "level": "Secondary School",
        "subjects": [
            "Mathematics",
            "English",
            "Physics",
            "Chemistry",
            "Biology",
            "Economics",
            "Government"
        ]
    }


@app.get("/university")
def university():
    return {
        "level": "University",
        "faculties": [
            "Engineering",
            "Medical Sciences",
            "Sciences",
            "Arts",
            "Management Sciences"
        ]
    }


@app.get("/features")
def features():
    return {
        "features": [
            "AI Tutor",
            "Homework Scanner",
            "Essay Submission",
            "Exam Practice",
            "Study Planner"
        ]
    }
