#!/bin/bash
set -e

echo "Build da aplicação..."
docker compose -f docker-compose.prod.yml build

echo "Subindo infraestrutura..."
docker compose -f docker-compose.prod.yml up -d

echo "Aguardando healthcheck..."
sleep 20

echo "Verificando aplicação..."
curl -f http://localhost/health && echo "Deploy OK!"
