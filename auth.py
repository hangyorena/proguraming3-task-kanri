from flask import Blueprint, render_template, request, redirect, session
import json
import os
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(BASE_DIR, "data", "users.json")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USER_FILE = os.path.join(BASE_DIR, "data", "users.json")
TASK_FILE = os.path.join(BASE_DIR, "data", "tasks.json")

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

    # タスク読込
    with open(TASK_FILE, "r", encoding="utf-8") as file:
        tasks = json.load(file)

    today = datetime.today().date()

    notices = []

    for task in tasks:

        deadline = datetime.strptime(
            task["deadline"],
            "%Y-%m-%d"
        ).date()

        remain = (deadline - today).days

        if 0 <= remain <= 7:
            task["notice"] = f"あと{remain}日"
            notices.append(task)

    return render_template(
        "home.html",
        username=session["username"],
        notices=notices
    )

# ログアウト
@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")
