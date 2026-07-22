from flask import Flask, render_template
import json

app = Flask(__name__)

# -----------------------------
# タスク一覧
# -----------------------------
@app.route("/")
def task_list():

    # JSONファイルを開く
    with open("data/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

    # HTMLへ渡す
    return render_template(
        "task_list.html",
        tasks=tasks
    )
@app.route("/task/add")
def task_add():

    return render_template("task_add.html")

if __name__ == "__main__":
    app.run(debug=True)
@app.route("/delete/<int:id>")
def delete_task(id):

    # JSON読み込み
    with open("data/tasks.json","r",encoding="utf-8") as file:
        tasks = json.load(file)

    # 指定されたID以外を残す
    tasks = [task for task in tasks if task["id"] != id]

    # 保存
    with open("data/tasks.json","w",encoding="utf-8") as file:
        json.dump(tasks,file,ensure_ascii=False,indent=4)

    # 一覧へ戻る
    return redirect("/")
@app.route("/edit/<int:id>")
def edit_task(id):

    # JSON読み込み
    with open("data/tasks.json", "r", encoding="utf-8") as file:
        tasks = json.load(file)

    # 編集するタスクを探す
    task = next((t for t in tasks if t["id"] == id), None)

    return render_template("task_edit.html", task=task)
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

    return redirect("/")
