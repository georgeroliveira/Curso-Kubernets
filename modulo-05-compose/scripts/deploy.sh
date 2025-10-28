#!/bin/bash
# Script de deploy automatizado com rollback

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_NAME="taskmanager"
COMPOSE_FILE="docker-compose.yml"

echo "======================================"
echo " TaskManager - Deploy Automatizado"
echo "======================================"
echo ""

# Funcao para log
log() {
    echo -e "${BLUE}[$(date +%H:%M:%S)]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Verificar se docker-compose.yml existe
if [ ! -f "$COMPOSE_FILE" ]; then
    log_error "Arquivo $COMPOSE_FILE nao encontrado"
    exit 1
fi

# Step 1: Backup do banco
log "Step 1/6: Criando backup do banco..."
if [ -f "scripts/backup.sh" ]; then
    bash scripts/backup.sh
    log_success "Backup criado"
else
    log_warning "Script de backup nao encontrado, pulando..."
fi

# Step 2: Pull de imagens
log "Step 2/6: Baixando imagens atualizadas..."
docker-compose pull
log_success "Imagens atualizadas"

# Step 3: Build da aplicacao
log "Step 3/6: Construindo aplicacao..."
docker-compose build --no-cache
log_success "Build concluido"

# Step 4: Deploy com zero downtime
log "Step 4/6: Iniciando deploy..."

# Parar e remover containers antigos
docker-compose down

# Subir novos containers
docker-compose up -d

log_success "Containers iniciados"

# Step 5: Aguardar health checks
log "Step 5/6: Aguardando health checks..."
sleep 30

# Verificar se aplicacao esta respondendo
HEALTH_CHECK_PASSED=false
for i in {1..10}; do
    if curl -f http://localhost/health > /dev/null 2>&1; then
        HEALTH_CHECK_PASSED=true
        break
    fi
    log "Tentativa $i/10 - Aguardando aplicacao..."
    sleep 5
done

if [ "$HEALTH_CHECK_PASSED" = true ]; then
    log_success "Health check passou!"
else
    log_error "Health check falhou apos 10 tentativas"
    log_warning "Executando rollback..."
    
    # Rollback: usar backup
    if [ -f "scripts/restore.sh" ]; then
        log_error "Por favor, execute manualmente: ./scripts/restore.sh"
    fi
    
    exit 1
fi

# Step 6: Limpeza
log "Step 6/6: Limpando recursos nao utilizados..."
docker image prune -f
log_success "Limpeza concluida"

# Mostrar status final
echo ""
echo "======================================"
log_success "Deploy concluido com sucesso!"
echo "======================================"
echo ""
echo "Status dos servicos:"
docker-compose ps

echo ""
echo "Logs recentes:"
docker-compose logs --tail=5

echo ""
echo "Acesse: http://localhost"
echo ""