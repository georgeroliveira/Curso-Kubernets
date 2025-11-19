#!/bin/bash

echo "[M08] Limpando cache do Grafana..."

docker exec grafana rm -rf /var/lib/grafana/plugins/*
docker restart grafana

echo "[OK] Cache limpo."
