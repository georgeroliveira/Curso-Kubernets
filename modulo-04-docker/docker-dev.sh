#!/bin/bash

echo "TaskManager - Docker Development"
echo "================================"

# Build da imagem
echo "Building image..."
docker build -t taskmanager:dev .

if [ $? -ne 0 ]; then
    echo "Error: Build failed"
    exit 1
fi

# Para container existente se houver
echo "Stopping existing container..."
docker stop taskmanager-dev 2>/dev/null || true
docker rm taskmanager-dev 2>/dev/null || true

# Criar volume se nao existir
echo "Creating volume..."
docker volume create taskmanager-data 2>/dev/null || true

# Executar container
echo "Starting container..."
docker run -d \
  --name taskmanager-dev \
  -p 5000:5000 \
  -v taskmanager-data:/app/data \
  taskmanager:dev

if [ $? -ne 0 ]; then
    echo "Error: Failed to start container"
    exit 1
fi

echo ""
echo "Success! TaskManager is running."
echo "================================"
echo "URL: http://localhost:5000"
echo "Health check: http://localhost:5000/health"
echo "Metrics: http://localhost:5000/metrics"
echo ""
echo "Useful commands:"
echo "  docker logs -f taskmanager-dev    # View logs"
echo "  docker stop taskmanager-dev       # Stop container"
echo "  docker exec -it taskmanager-dev bash  # Enter container"
echo ""