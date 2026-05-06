from flask import Flask, request, jsonify
import os
from openai import OpenAI
import wolframalpha

app = Flask(__name__)

# Load env variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
WOLFRAM_APP_ID = os.environ.get("WOLFRAM_APP_ID")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY")

if not WOLFRAM_APP_ID:
    raise ValueError("Missing WOLFRAM_APP_ID")

# Initialize APIs
client = OpenAI(api_key=OPENAI_API_KEY)
wolfram = wolframalpha.Client(WOLFRAM_APP_ID)


def ask_ai(q):
    try:
        res = wolfram.query(q)
        return next(res.results).text
    except:
        try:
            r = client.chat.completions.create(
                model="gpt-5.3-mini",
                messages=[{"role": "user", "content": q}],
                max_tokens=200
            )
            return r.choices[0].message.content.strip()
        except:
            return "Error getting answer"


@app.route("/")
def home():
    return "Homework Hero API is running 🚀"


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = ask_ai(question)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run()
