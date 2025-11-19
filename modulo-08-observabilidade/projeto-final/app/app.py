from flask import Flask, jsonify, request
from metrics import http_requests_total, http_request_duration_seconds, tasks_total
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

tasks = []

@app.before_request
def before():
    request.start = time.time()

@app.after_request
def after(response):
    duration = time.time() - request.start

    http_requests_total.labels(method=request.method, endpoint=request.path).inc()
    http_request_duration_seconds.labels(endpoint=request.path).observe(duration)
    tasks_total.set(len(tasks))

    return response

@app.route("/")
def index():
    return jsonify({"msg": "TaskManager API"})

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
