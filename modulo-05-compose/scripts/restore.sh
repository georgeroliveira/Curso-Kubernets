#!/bin/bash
set -e

if [ -z "\$1" ]; then
    echo "Uso: restore.sh arquivo.sql"
    exit 1
fi

docker exec -i \$(docker ps -qf "name=db") psql -U taskuser taskdb < "\$1"

echo "Restore concluído."
