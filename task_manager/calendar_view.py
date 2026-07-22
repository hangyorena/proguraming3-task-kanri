from flask import Blueprint, render_template, abort, request
import calendar
import json
import os
from datetime import datetime

calendar_bp = Blueprint("calendar", __name__)

DATA_FILE = os.path.join("data", "tasks.json")

# JSON読込
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 前月・翌月
def get_prev_next(year, month):

    if month == 1:
        prev_year = year - 1
        prev_month = 12
    else:
        prev_year = year
        prev_month = month - 1

    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1

    return prev_year, prev_month, next_year, next_month

# 通知
def create_notifications(tasks):

    today = datetime.today().date()

    notice = []

    for task in tasks:

        deadline = datetime.strptime(
            task["deadline"],
            "%Y-%m-%d"
        ).date()

        remain = (deadline - today).days

        if remain == 2:
            task["notice"] = "締切まであと2日"
            notice.append(task)

        elif remain == 1:
            task["notice"] = "締切まであと1日"
            notice.append(task)

    return notice

# カレンダー画面
@calendar_bp.route("/calendar")
def calendar_view():

    now = datetime.today()

    year = request.args.get(
        "year",
        default=now.year,
        type=int
    )

    month = request.args.get(
        "month",
        default=now.month,
        type=int
    )

    cal = calendar.monthcalendar(year, month)

    tasks = load_tasks()

    notices = create_notifications(tasks)

    if now.year == year and now.month == month:
        today_day = now.day
    else:
        today_day = -1

    prev_y, prev_m, next_y, next_m = get_prev_next(
        year,
        month
    )

    return render_template(
        "calendar.html",
        year=year,
        month=month,
        cal=cal,
        tasks=tasks,
        today=today_day,
        notices=notices,
        prev_year=prev_y,
        prev_month=prev_m,
        next_year=next_y,
        next_month=next_m
    )

# タスク詳細
@calendar_bp.route("/task/<int:task_id>")
def task_detail(task_id):

    tasks = load_tasks()

    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        abort(404)

    return render_template(
        "task_detail.html",
        task=task
    )
