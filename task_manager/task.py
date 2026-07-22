from flask import Blueprint, render_template, request, redirect
import json
import os

# Blueprintを作成
task_bp = Blueprint("task", __name__)

# JSONファイルの場所
DATA_FILE = "data/tasks.json"


# -------------------------------
# JSON読み込み
# -------------------------------
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# -------------------------------
# JSON保存
# -------------------------------
def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


# -------------------------------
# タスク一覧
# -------------------------------
@task_bp.route("/")
def task_list():

    tasks = load_tasks()

    return render_template(
        "task_list.html",
        tasks=tasks
    )


# -------------------------------
# タスク追加画面
# -------------------------------
@task_bp.route("/task/add")
def task_add():

    return render_template("task_add.html")


# -------------------------------
# タスク追加
# -------------------------------
@task_bp.route("/add", methods=["POST"])
def add_task():

    tasks = load_tasks()

    if len(tasks) == 0:
        new_id = 1
    else:
        new_id = max(task["id"] for task in tasks) + 1

    new_task = {

        "id": new_id,

        "title": request.form["title"],

        "person": request.form["person"],

        "deadline": request.form["deadline"],

        "status": request.form["status"],

        "detail": request.form["detail"]

    }

    tasks.append(new_task)

    save_tasks(tasks)

    return redirect("/")


# -------------------------------
# 編集画面
# -------------------------------
@task_bp.route("/edit/<int:id>")
def edit_task(id):

    tasks = load_tasks()

    task = next((t for t in tasks if t["id"] == id), None)

    return render_template(
        "task_edit.html",
        task=task
    )


# -------------------------------
# 更新
# -------------------------------
@task_bp.route("/update/<int:id>", methods=["POST"])
def update_task(id):

    tasks = load_tasks()

    for task in tasks:

        if task["id"] == id:

            task["title"] = request.form["title"]
            task["person"] = request.form["person"]
            task["deadline"] = request.form["deadline"]
            task["status"] = request.form["status"]
            task["detail"] = request.form["detail"]

            break

    save_tasks(tasks)

    return redirect("/")


# -------------------------------
# 削除
# -------------------------------
@task_bp.route("/delete/<int:id>")
def delete_task(id):

    tasks = load_tasks()

    tasks = [task for task in tasks if task["id"] != id]

    save_tasks(tasks)

    return redirect("/")
