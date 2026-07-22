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


if __name__ == "__main__":
    app.run(debug=True)
