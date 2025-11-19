#!/bin/bash

echo "[M08] Injetando carga na aplicação (bench)..."

for i in {1..200}; do
    curl -s http://localhost:5000/health > /dev/null
    curl -s -X POST http://localhost:5000/api/tasks -H 'Content-Type: application/json' -d '{"title":"Carga-'$i'"}' > /dev/null
done

echo "[OK] Carga gerada."
