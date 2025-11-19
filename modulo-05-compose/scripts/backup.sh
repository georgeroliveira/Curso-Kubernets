#!/bin/bash
set -e

BACKUP_DIR="backups"
mkdir -p \$BACKUP_DIR

FILE="\$BACKUP_DIR/db_\$(date +%Y%m%d_%H%M%S).sql"

docker exec \$(docker ps -qf "name=db") pg_dump -U taskuser taskdb > \$FILE

echo "Backup criado: \$FILE"
