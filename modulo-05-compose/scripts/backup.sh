#!/bin/bash
# Script de backup do PostgreSQL

set -e  # Parar em caso de erro

# Configuracoes
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/taskmanager_${DATE}.sql"
CONTAINER_NAME="taskmanager-db"
DB_NAME="taskdb"
DB_USER="taskuser"

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "======================================"
echo " TaskManager - Backup Database"
echo "======================================"
echo ""

# Criar diretorio de backup
mkdir -p ${BACKUP_DIR}

# Verificar se container esta rodando
if ! docker ps | grep -q ${CONTAINER_NAME}; then
    echo -e "${RED}ERRO: Container ${CONTAINER_NAME} nao esta rodando${NC}"
    exit 1
fi

echo "Iniciando backup..."
echo "Data/Hora: $(date)"
echo "Container: ${CONTAINER_NAME}"
echo "Database: ${DB_NAME}"
echo ""

# Realizar backup
docker exec -t ${CONTAINER_NAME} pg_dump -U ${DB_USER} ${DB_NAME} > ${BACKUP_FILE}

if [ $? -eq 0 ]; then
    # Compactar backup
    gzip ${BACKUP_FILE}
    BACKUP_FILE="${BACKUP_FILE}.gz"
    
    # Calcular tamanho
    SIZE=$(du -h ${BACKUP_FILE} | cut -f1)
    
    echo -e "${GREEN}Backup realizado com sucesso!${NC}"
    echo "Arquivo: ${BACKUP_FILE}"
    echo "Tamanho: ${SIZE}"
    
    # Manter apenas ultimos 7 backups
    echo ""
    echo "Limpando backups antigos (mantendo ultimos 7)..."
    ls -t ${BACKUP_DIR}/*.sql.gz 2>/dev/null | tail -n +8 | xargs -r rm
    
    echo ""
    echo "Backups disponiveis:"
    ls -lh ${BACKUP_DIR}/*.sql.gz 2>/dev/null || echo "Nenhum backup encontrado"
else
    echo -e "${RED}ERRO: Falha ao realizar backup${NC}"
    exit 1
fi

echo ""
echo "======================================"
echo " Backup concluido!"
echo "======================================"