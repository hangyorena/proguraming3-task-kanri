from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "task_manager_secret"

# -----------------------------
# ログイン画面
# -----------------------------
@app.route("/")
def login():
    return render_template("login.html")


# -----------------------------
# ログイン認証
# -----------------------------
@app.route("/login", methods=["POST"])
def login_check():

    username = request.form["username"]
    password = request.form["password"]

    with open("data/users.json", "r", encoding="utf-8") as file:
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


# -----------------------------
# ホーム画面
# -----------------------------
@app.route("/home")
def home():

    if "username" not in session:
        return redirect("/")

    return render_template(
        "home.html",
        username=session["username"]
    )


# -----------------------------
# ログアウト
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# -----------------------------
# タスク一覧
# -----------------------------
@app.route("/task")
def task_list():

    with open("data/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

    return render_template(
        "task_list.html",
        tasks=tasks
    )


# -----------------------------
# タスク追加画面
# -----------------------------
@app.route("/task/add")
def task_add():

    return render_template("task_add.html")


# -----------------------------
# タスク削除
# -----------------------------
@app.route("/delete/<int:id>")
def delete_task(id):

    with open("data/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

    tasks = [task for task in tasks if task["id"] != id]

    with open("data/tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

    return redirect("/task")


# -----------------------------
# タスク編集画面
# -----------------------------
@app.route("/edit/<int:id>")
def edit_task(id):

    with open("data/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

    task = next((t for t in tasks if t["id"] == id), None)

    return render_template(
        "task_edit.html",
        task=task
    )


# -----------------------------
# タスク更新
# -----------------------------
@app.route("/update/<int:id>", methods=["POST"])
def update_task(id):

    with open("data/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

    for task in tasks:

        if task["id"] == id:

            task["title"] = request.form["title"]
            task["person"] = request.form["person"]
            task["deadline"] = request.form["deadline"]
            task["status"] = request.form["status"]
            task["detail"] = request.form["detail"]

            break

    with open("data/tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

    return redirect("/task")


if __name__ == "__main__":
    app.run(debug=True)
