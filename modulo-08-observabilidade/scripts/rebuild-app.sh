#!/bin/bash

echo "[M08] Rebuild da aplicação..."

docker build -t taskmanager-app:latest projeto-taskmanager
docker compose -f docker-compose.observabilidade.yml up -d --force-recreate app

echo "[OK] Aplicação recarregada."
