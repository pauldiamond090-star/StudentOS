from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="School App")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Welcome to Redford School App</h1>
    <p>Your app is working successfully.</p>
    """
