import os
import psycopg2
import redis
import logging
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from config import get_config

config = get_config()
app = Flask(__name__)

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger("taskmanager")

# PostgreSQL
conn = psycopg2.connect(config.DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
)
""")
conn.commit()

# Redis
cache = redis.from_url(config.REDIS_URL)

@app.route("/")
def index():
    cursor.execute("SELECT id, title, completed FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks, version=config.VERSION, environment=config.ENVIRONMENT)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
    conn.commit()
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    cursor.execute("UPDATE tasks SET completed = TRUE, completed_at = NOW() WHERE id = %s", (task_id,))
    conn.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {
        "status": "healthy",
        "db": "ok",
        "redis": "ok" if cache.ping() else "fail",
        "version": config.VERSION,
        "environment": config.ENVIRONMENT
    }

if __name__ == "__main__":
    logger.info(f"Iniciando TaskManager v{config.VERSION}")
    app.run(host=config.HOST, port=config.PORT)
