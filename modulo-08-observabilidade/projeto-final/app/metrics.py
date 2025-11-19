from prometheus_client import Counter, Histogram, Gauge

http_requests_total = Counter(
    "http_requests_total",
    "Total de requisições HTTP",
    ["method", "endpoint"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "Duração das requisições HTTP",
    ["endpoint"]
)

tasks_total = Gauge(
    "tasks_total",
    "Total de tarefas"
)
