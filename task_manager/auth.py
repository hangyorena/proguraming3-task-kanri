from flask import Blueprint, render_template, request, redirect, session
import json
import os

auth_bp = Blueprint("auth", __name__)

USER_FILE = os.path.join("data", "users.json")

# ログイン画面
@auth_bp.route("/")
def login():
    return render_template("login.html")

# ログイン認証
@auth_bp.route("/login", methods=["POST"])
def login_check():

    username = request.form["username"]
    password = request.form["password"]

    with open(USER_FILE, "r", encoding="utf-8") as file:
        users = json.load(file)

    for user in users:
        if user["username"] == username and user["password"] == password:

            session["username"] = user["name"]
            session["role"] = user["role"]

            return redirect("/home")

    return render_template(
        "login.html",
        error="ユーザー名またはパスワードが違います"
    )

# ホーム画面
@auth_bp.route("/home")
def home():

    if "username" not in session:
        return redirect("/")

    return render_template(
        "home.html",
        username=session["username"]
    )

# ログアウト
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")
