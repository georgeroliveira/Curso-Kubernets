from flask import Flask, render_template, request, redirect, url_for
from config import get_config

app = Flask(__name__)
config = get_config()

tasks = []
next_id = 1

@app.route("/")
def index():
    return render_template("index.html", 
                           tasks=tasks,
                           version=config.VERSION,
                           environment=config.ENVIRONMENT)

@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    title = request.form.get("title")

    if title:
        tasks.append({
            "id": next_id,
            "title": title,
            "completed": False
        })
        next_id += 1

    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
