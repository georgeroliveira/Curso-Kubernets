#!/bin/bash
ARQ="snapshot-$(date +%Y%m%d-%H%M%S).txt"

echo "[M08] Coletando métricas..."
curl -s http://localhost:5000/metrics > "$ARQ"

echo "[OK] Snapshot salvo em: $ARQ"
