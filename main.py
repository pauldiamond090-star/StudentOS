from flask import Flask, render_template

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Login Page
@app.route("/login")
def login():
    return render_template("login.html")

# Register Page
@app.route("/register")
def register():
    return render_template("register.html")

# Student Dashboard
@app.route("/student-dashboard")
def student_dashboard():
    return render_template("Student_dashboard.html")

# Teacher Dashboard
@app.route("/teacher-dashboard")
def teacher_dashboard():
    return render_template("teacher_dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
