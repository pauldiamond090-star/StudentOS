from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Flask App Deployed Successfully 🚀</h1>
    <p>Your Railway deployment is working.</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
