#!/bin/bash

echo "[DEPLOY] Atualizando imagem..."
docker compose pull

echo "[DEPLOY] Subindo serviços..."
docker compose up -d --remove-orphans

echo "[DEPLOY] Finalizado."
