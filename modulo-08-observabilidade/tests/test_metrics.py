import requests

def test_metrics():
    r = requests.get("http://localhost:5000/metrics")
    assert r.status_code == 200
