#!/bin/bash

echo "[M08] Simulando alerta: derrubando app..."

docker stop taskmanager-app &> /dev/null || true
sleep 5

echo "[OK] App parado. Verifique os alerts no Prometheus."
