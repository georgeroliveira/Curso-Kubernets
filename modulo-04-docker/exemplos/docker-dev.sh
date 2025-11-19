#!/bin/bash
echo "TaskManager - Docker Development (Permissões Corrigidas)"
echo "========================================================"

# Detecta o ID do usuário atual para evitar problemas de permissão nos volumes
USER_ID=$(id -u)
GROUP_ID=$(id -g)

echo "Building image..."
docker build -t taskmanager:dev .

# Remove container anterior se existir
docker stop taskmanager-dev 2>/dev/null || true
docker rm taskmanager-dev 2>/dev/null || true

echo "Iniciando container com UID: $USER_ID..."

# Roda o container passando o usuário atual
docker run -d \
  --name taskmanager-dev \
  --user $USER_ID:$GROUP_ID \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -e HOME=/app \
  taskmanager:dev

echo ""
echo "Container rodando!"
echo "Logs: docker logs -f taskmanager-dev"