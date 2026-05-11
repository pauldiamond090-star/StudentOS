from flask import Flask, render_template_string, request

app = Flask(__name__)

homework_tips = {
    "math": "Break the problem into smaller steps and solve carefully.",
    "physics": "Draw diagrams and identify known formulas first.",
    "chemistry": "Memorize key formulas and practice balancing equations.",
    "english": "Read the question carefully and structure your answer clearly."
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Homework Hero</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            padding: 40px;
            text-align: center;
        }

        .box {
            background: white;
            padding: 30px;
            border-radius: 10px;
            width: 80%;
            margin: auto;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }

        input {
            padding: 10px;
            width: 60%;
            margin-top: 20px;
        }

        button {
            padding: 10px 20px;
            background: #222;
            color: white;
            border: none;
            margin-top: 15px;
            cursor: pointer;
        }

        .result {
            margin-top: 25px;
            font-size: 18px;
            color: green;
        }
    </style>
</head>
<body>

<div class="box">
    <h1>📚 Homework Hero</h1>
    <p>Your AI Homework Helper</p>

    <form method="POST">
        <input type="text" name="subject" placeholder="Enter subject e.g. math">
        <br>
        <button type="submit">Get Help</button>
    </form>

    {% if answer %}
        <div class="result">
            {{ answer }}
        </div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":
        subject = request.form.get("subject", "").lower()

        answer = homework_tips.get(
            subject,
            "Sorry, no homework tips found for that subject yet."
        )

    return render_template_string(HTML, answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
