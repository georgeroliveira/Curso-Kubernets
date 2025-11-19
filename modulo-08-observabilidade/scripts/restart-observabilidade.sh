#!/bin/bash
set -e

echo "[M08] Reiniciando stack de observabilidade..."
docker compose -f docker-compose.observabilidade.yml down
docker compose -f docker-compose.observabilidade.yml up -d

echo "[OK] Stack reiniciada."
