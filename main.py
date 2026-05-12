from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/splash")
def splash():
    return render_template("splash.html")


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        return redirect("/register")

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        return "Registration Successful"

    return render_template("register.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
