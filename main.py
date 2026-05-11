from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return """
    <h1>Login Page</h1>
    <p>StudentOS Login System Coming Soon</p>
    """

@app.route("/register")
def register():
    return """
    <h1>Register Page</h1>
    <p>StudentOS Registration System Coming Soon</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
