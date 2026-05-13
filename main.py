from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="StudentOS")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>StudentOS Login</title>
    </head>
    <body>

    <h1>StudentOS Login</h1>

    <form>
        <input type="text" placeholder="Username">

        <br><br>

        <input type="password" placeholder="Password">

        <br><br>

        <button type="submit">
            Login
        </button>
    </form>

    </body>
    </html>
    """
