#!/bin/bash
# Script de restore do PostgreSQL

set -e

BACKUP_DIR="./backups"
CONTAINER_NAME="taskmanager-db"
DB_NAME="taskdb"
DB_USER="taskuser"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "======================================"
echo " TaskManager - Restore Database"
echo "======================================"
echo ""

# Listar backups disponiveis
echo "Backups disponiveis:"
echo ""
ls -lht ${BACKUP_DIR}/*.sql.gz 2>/dev/null | awk '{print NR ") " $9 " (" $5 ", " $6 " " $7 ")"}' || {
    echo -e "${RED}Nenhum backup encontrado em ${BACKUP_DIR}${NC}"
    exit 1
}
echo ""

# Solicitar qual backup restaurar
read -p "Digite o numero do backup para restaurar (ou 'q' para sair): " choice

if [ "$choice" = "q" ]; then
    echo "Operacao cancelada."
    exit 0
fi

# Obter arquivo selecionado
BACKUP_FILE=$(ls -t ${BACKUP_DIR}/*.sql.gz 2>/dev/null | sed -n "${choice}p")

if [ -z "$BACKUP_FILE" ]; then
    echo -e "${RED}ERRO: Backup invalido${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}ATENCAO: Esta operacao ira SOBRESCREVER todos os dados atuais!${NC}"
echo "Backup selecionado: $BACKUP_FILE"
echo ""
read -p "Tem certeza que deseja continuar? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Operacao cancelada."
    exit 0
fi

echo ""
echo "Iniciando restore..."

# Parar aplicacao
echo "Parando aplicacao..."
docker-compose stop app1 app2 app3

# Descompactar backup
echo "Descompactando backup..."
TEMP_FILE="${BACKUP_FILE%.gz}"
gunzip -c ${BACKUP_FILE} > ${TEMP_FILE}

# Realizar restore
echo "Restaurando database..."
cat ${TEMP_FILE} | docker exec -i ${CONTAINER_NAME} psql -U ${DB_USER} -d ${DB_NAME}

# Limpar arquivo temporario
rm ${TEMP_FILE}

# Reiniciar aplicacao
echo "Reiniciando aplicacao..."
docker-compose start app1 app2 app3

echo ""
echo -e "${GREEN}Restore concluido com sucesso!${NC}"
echo ""
echo "======================================"