from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from config import config

app = Flask(__name__)

tasks = []
next_id = 1

@app.route('/')
def index():
    return render_template(
        'index.html',
        tasks=tasks,
        version=config.VERSION,
        environment=config.ENVIRONMENT
    )

@app.route('/add', methods=['POST'])
def add():
    global next_id
    title = request.form.get('title')
    if title:
        tasks.append({
            'id': next_id,
            'title': title,
            'completed': False,
            'created_at': datetime.now().isoformat()
        })
        next_id += 1
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    for t in tasks:
        if t['id'] == task_id:
            t['completed'] = True
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect(url_for('index'))

@app.route('/health')
def health():
    return {"status": "ok", "version": config.VERSION}

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
