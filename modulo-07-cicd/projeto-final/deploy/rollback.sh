#!/bin/bash

echo "[ROLLBACK] Voltando para versão anterior..."

docker compose down
docker compose up -d

echo "[ROLLBACK] Concluído."
