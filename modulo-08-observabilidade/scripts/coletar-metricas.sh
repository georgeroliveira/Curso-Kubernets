#!/bin/bash

echo "[M08] Coletando métricas..."
curl -s http://localhost:5000/metrics | head -50
