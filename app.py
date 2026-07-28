from flask import Flask
from auth import auth_bp
from task import task_bp
from calendar_view import calendar_bp

app = Flask(__name__)
app.secret_key = "task_manager_secret"

# Blueprint登録
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
app.register_blueprint(calendar_bp)

if __name__ == "__main__":
    app.run(debug=True)
