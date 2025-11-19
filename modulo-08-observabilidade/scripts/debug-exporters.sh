#!/bin/bash

echo "[M08] Testando exporters..."

echo "- App Exporter (5000/metrics):"
curl -s http://localhost:5000/metrics | head -20

echo
echo "- Prometheus Target Status:"
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[].health'
