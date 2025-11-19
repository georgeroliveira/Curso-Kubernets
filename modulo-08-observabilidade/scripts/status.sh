#!/bin/bash

echo "[M08] Status da stack:"
docker compose -f docker-compose.observabilidade.yml ps

echo
echo "Portas:"
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3000"
