from flask import Flask, redirect, request, session, url_for, render_template
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

CLIENT_ID = os.getenv("CANVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("CANVA_CLIENT_SECRET")
REDIRECT_URI = os.getenv("CANVA_REDIRECT_URI")

AUTH_URL = "https://www.canva.com/api/oauth/authorize"
TOKEN_URL = "https://api.canva.com/api/oauth/token"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login")
def login():
    auth_link = (
        f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_link)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed.", 400

    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
        },
    )
    token_data = response.json()
    session["access_token"] = token_data.get("access_token")
    return render_template("home.html", token=token_data)

if __name__ == "__main__":
    app.run(debug=True)
