#!/bin/bash

echo "[M08] Validando prometheus.yml..."
docker run --rm -v $(pwd):/etc/prometheus prom/prometheus promtool check config /etc/prometheus/prometheus.yml
