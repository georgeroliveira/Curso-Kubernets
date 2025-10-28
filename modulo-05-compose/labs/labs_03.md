# Lab 03 - Produção Ready

**Duração:** 60 minutos  
**Dificuldade:** Intermediário/Avançado

## Objetivos

Ao final deste lab você será capaz de:
- Implementar health checks avançados em todos os serviços
- Configurar logs estruturados e centralizados
- Criar scripts de backup e restore automatizados
- Implementar script de deploy com rollback
- Configurar ambiente de produção
- Aplicar boas práticas de segurança
- Preparar aplicação para deploy real

## Pré-requisitos

- Lab 01 e Lab 02 concluídos
- Stack com Nginx + 3 instâncias rodando
- Conhecimento de shell script (bash/PowerShell)

## Parte 1: Health Checks Avançados (15 min)

### 1.1 Melhorar health check da aplicação

**Atualizar app.py com health check completo:**

```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import redis
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configurações
DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
INSTANCE_ID = os.getenv('INSTANCE_ID', 'unknown')
INSTANCE_NAME = os.getenv('INSTANCE_NAME', 'Unknown Instance')

# Startup time
STARTUP_TIME = datetime.now()

# Conexão Redis
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    print(f"[{INSTANCE_ID}] Redis connected successfully!")
except Exception as e:
    print(f"[{INSTANCE_ID}] Redis connection failed: {e}")
    redis_client = None

def get_db():
    """Retorna conexão com o banco"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

@app.route('/health')
def health():
    """Health check detalhado"""
    start_time = time.time()
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': (datetime.now() - STARTUP_TIME).total_seconds(),
        'instance': {
            'id': INSTANCE_ID,
            'name': INSTANCE_NAME,
            'started_at': STARTUP_TIME.isoformat()
        },
        'checks': {},
        'metrics': {}
    }
    
    # Check 1: PostgreSQL
    db_start = time.time()
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT 1 as health_check')
        result = cur.fetchone()
        
        # Contar tarefas no banco
        cur.execute('SELECT COUNT(*) as total FROM tasks')
        task_count = cur.fetchone()
        
        cur.close()
        conn.close()
        
        health_status['checks']['database'] = {
            'status': 'healthy',
            'response_time_ms': round((time.time() - db_start) * 1000, 2),
            'tasks_count': task_count['total'] if task_count else 0
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e),
            'response_time_ms': round((time.time() - db_start) * 1000, 2)
        }
    
    # Check 2: Redis
    redis_start = time.time()
    try:
        if redis_client:
            redis_client.ping()
            
            # Info do Redis
            info = redis_client.info('stats')
            
            health_status['checks']['redis'] = {
                'status': 'healthy',
                'response_time_ms': round((time.time() - redis_start) * 1000, 2),
                'total_commands': info.get('total_commands_processed', 0),
                'connected_clients': info.get('connected_clients', 0)
            }
        else:
            health_status['checks']['redis'] = {
                'status': 'not_configured',
                'message': 'Redis client not initialized'
            }
    except Exception as e:
        health_status['checks']['redis'] = {
            'status': 'unhealthy',
            'error': str(e),
            'response_time_ms': round((time.time() - redis_start) * 1000, 2)
        }
    
    # Check 3: Disco (opcional)
    try:
        import shutil
        disk = shutil.disk_usage('/app')
        health_status['checks']['disk'] = {
            'status': 'healthy',
            'total_gb': round(disk.total / (1024**3), 2),
            'used_gb': round(disk.used / (1024**3), 2),
            'free_gb': round(disk.free / (1024**3), 2),
            'percent_used': round((disk.used / disk.total) * 100, 2)
        }
    except Exception as e:
        health_status['checks']['disk'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Métricas gerais
    health_status['metrics']['total_response_time_ms'] = round((time.time() - start_time) * 1000, 2)
    
    # Status final
    unhealthy_checks = [k for k, v in health_status['checks'].items() 
                       if isinstance(v, dict) and v.get('status') == 'unhealthy']
    
    if unhealthy_checks:
        health_status['status'] = 'unhealthy'
        health_status['unhealthy_services'] = unhealthy_checks
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

@app.route('/ready')
def readiness():
    """Readiness probe - verifica se pode receber tráfego"""
    try:
        # Verificar apenas se consegue conectar nos serviços essenciais
        conn = get_db()
        conn.close()
        
        if redis_client:
            redis_client.ping()
        
        return jsonify({
            'status': 'ready',
            'instance': INSTANCE_ID
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'error': str(e)
        }), 503

@app.route('/live')
def liveness():
    """Liveness probe - verifica se está vivo (não travado)"""
    return jsonify({
        'status': 'alive',
        'instance': INSTANCE_ID,
        'timestamp': datetime.now().isoformat()
    }), 200

# ... resto do código (index, add_task, etc) permanece igual ...
```

### 1.2 Atualizar docker-compose.yml com novos health checks

**Modificar seção de health checks das apps:**

```yaml
  app1:
    # ... configurações existentes ...
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/ready"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 30s
```

## Parte 2: Logs Estruturados (15 min)

### 2.1 Implementar logging estruturado

**Criar arquivo logger.py no taskmanager/:**

**Linux/Mac:**
```bash
cat > taskmanager/logger.py << 'EOF'
import logging
import json
import os
from datetime import datetime

class StructuredLogger:
    """Logger que produz logs em formato JSON estruturado"""
    
    def __init__(self, name='taskmanager'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Criar diretório de logs
        log_dir = '/app/logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # Handler para arquivo JSON
        json_handler = logging.FileHandler(f'{log_dir}/app.json.log')
        json_handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Handler para console (desenvolvimento)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        self.logger.addHandler(json_handler)
        self.logger.addHandler(console_handler)
        
        # Informações da instância
        self.instance_id = os.getenv('INSTANCE_ID', 'unknown')
    
    def _build_log_entry(self, level, message, **kwargs):
        """Constrói entrada de log estruturada"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'instance': self.instance_id,
            'message': message,
            **kwargs
        }
        return json.dumps(log_entry)
    
    def info(self, message, **kwargs):
        """Log level INFO"""
        self.logger.info(self._build_log_entry('INFO', message, **kwargs))
    
    def error(self, message, **kwargs):
        """Log level ERROR"""
        self.logger.error(self._build_log_entry('ERROR', message, **kwargs))
    
    def warning(self, message, **kwargs):
        """Log level WARNING"""
        self.logger.warning(self._build_log_entry('WARNING', message, **kwargs))
    
    def debug(self, message, **kwargs):
        """Log level DEBUG"""
        self.logger.debug(self._build_log_entry('DEBUG', message, **kwargs))

# Instância global do logger
logger = StructuredLogger()
EOF
```

**Windows (PowerShell):**
```powershell
# Mesmo conteúdo, usar editor ou:
# New-Item -Path taskmanager/logger.py -ItemType File
# Copiar o conteúdo acima
```

### 2.2 Usar logger no app.py

**Adicionar no início do app.py:**

```python
from logger import logger

# Substituir prints por logs estruturados
# Antes:
# print("Redis connected successfully!")

# Depois:
logger.info("Redis connected successfully", redis_url=REDIS_URL)

# Exemplos de uso:
@app.route('/add', methods=['POST'])
def add_task():
    user_id = 1
    title = request.form.get('title')
    
    logger.info("Task creation attempted", 
                user_id=user_id, 
                title=title,
                ip=request.remote_addr)
    
    try:
        # ... código de criar tarefa ...
        logger.info("Task created successfully",
                   task_id=task['id'],
                   title=title,
                   user_id=user_id)
    except Exception as e:
        logger.error("Task creation failed",
                    error=str(e),
                    user_id=user_id,
                    title=title)
```

## Parte 3: Scripts de Backup (15 min)

### 3.1 Criar script de backup

**Linux/Mac:**
```bash
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
# Script de backup do PostgreSQL

set -e  # Parar em caso de erro

# Configurações
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/taskmanager_${DATE}.sql"
CONTAINER_NAME="taskmanager-db"
DB_NAME="taskdb"
DB_USER="taskuser"

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "======================================"
echo " TaskManager - Backup Database"
echo "======================================"
echo ""

# Criar diretório de backup
mkdir -p ${BACKUP_DIR}

# Verificar se container está rodando
if ! docker ps | grep -q ${CONTAINER_NAME}; then
    echo -e "${RED}ERRO: Container ${CONTAINER_NAME} não está rodando${NC}"
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
    
    # Manter apenas últimos 7 backups
    echo ""
    echo "Limpando backups antigos (mantendo últimos 7)..."
    ls -t ${BACKUP_DIR}/*.sql.gz | tail -n +8 | xargs -r rm
    
    echo ""
    echo "Backups disponíveis:"
    ls -lh ${BACKUP_DIR}/*.sql.gz
else
    echo -e "${RED}ERRO: Falha ao realizar backup${NC}"
    exit 1
fi

echo ""
echo "======================================"
echo " Backup concluído!"
echo "======================================"
EOF

chmod +x scripts/backup.sh
```

**Windows (PowerShell):**
```powershell
@"
# Script de backup do PostgreSQL (Windows)

`$BACKUP_DIR = ".\backups"
`$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
`$BACKUP_FILE = "`$BACKUP_DIR\taskmanager_`$DATE.sql"
`$CONTAINER_NAME = "taskmanager-db"
`$DB_NAME = "taskdb"
`$DB_USER = "taskuser"

Write-Host "======================================"
Write-Host " TaskManager - Backup Database"
Write-Host "======================================"
Write-Host ""

# Criar diretório de backup
New-Item -Path `$BACKUP_DIR -ItemType Directory -Force | Out-Null

# Verificar se container está rodando
`$running = docker ps --filter "name=`$CONTAINER_NAME" --format "{{.Names}}"
if (-not `$running) {
    Write-Host "ERRO: Container `$CONTAINER_NAME não está rodando" -ForegroundColor Red
    exit 1
}

Write-Host "Iniciando backup..."
Write-Host "Data/Hora: `$(Get-Date)"
Write-Host "Container: `$CONTAINER_NAME"
Write-Host "Database: `$DB_NAME"
Write-Host ""

# Realizar backup
docker exec -t `$CONTAINER_NAME pg_dump -U `$DB_USER `$DB_NAME | Out-File -FilePath `$BACKUP_FILE -Encoding UTF8

if (`$LASTEXITCODE -eq 0) {
    # Compactar backup
    Compress-Archive -Path `$BACKUP_FILE -DestinationPath "`$BACKUP_FILE.zip"
    Remove-Item `$BACKUP_FILE
    
    `$BACKUP_FILE = "`$BACKUP_FILE.zip"
    `$SIZE = (Get-Item `$BACKUP_FILE).Length / 1MB
    
    Write-Host "Backup realizado com sucesso!" -ForegroundColor Green
    Write-Host "Arquivo: `$BACKUP_FILE"
    Write-Host "Tamanho: `$([math]::Round(`$SIZE, 2)) MB"
    
    # Manter apenas últimos 7 backups
    Write-Host ""
    Write-Host "Limpando backups antigos (mantendo últimos 7)..."
    Get-ChildItem `$BACKUP_DIR -Filter "*.zip" | 
        Sort-Object LastWriteTime -Descending | 
        Select-Object -Skip 7 | 
        Remove-Item
    
    Write-Host ""
    Write-Host "Backups disponíveis:"
    Get-ChildItem `$BACKUP_DIR -Filter "*.zip" | 
        Format-Table Name, @{Label="Tamanho";Expression={"`$([math]::Round(`$_.Length/1MB, 2)) MB"}}, LastWriteTime
} else {
    Write-Host "ERRO: Falha ao realizar backup" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================"
Write-Host " Backup concluído!"
Write-Host "======================================"
"@ | Out-File -FilePath scripts/backup.ps1 -Encoding UTF8
```

### 3.2 Criar script de restore

**Linux/Mac:**
```bash
cat > scripts/restore.sh << 'EOF'
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

# Listar backups disponíveis
echo "Backups disponíveis:"
echo ""
ls -lht ${BACKUP_DIR}/*.sql.gz | awk '{print NR ") " $9 " (" $5 ", " $6 " " $7 ")"}'
echo ""

# Solicitar qual backup restaurar
read -p "Digite o número do backup para restaurar (ou 'q' para sair): " choice

if [ "$choice" = "q" ]; then
    echo "Operação cancelada."
    exit 0
fi

# Obter arquivo selecionado
BACKUP_FILE=$(ls -t ${BACKUP_DIR}/*.sql.gz | sed -n "${choice}p")

if [ -z "$BACKUP_FILE" ]; then
    echo -e "${RED}ERRO: Backup inválido${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}ATENÇÃO: Esta operação irá SOBRESCREVER todos os dados atuais!${NC}"
echo "Backup selecionado: $BACKUP_FILE"
echo ""
read -p "Tem certeza que deseja continuar? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Operação cancelada."
    exit 0
fi

echo ""
echo "Iniciando restore..."

# Parar aplicação
echo "Parando aplicação..."
docker-compose stop app1 app2 app3

# Descompactar backup
echo "Descompactando backup..."
TEMP_FILE="${BACKUP_FILE%.gz}"
gunzip -c ${BACKUP_FILE} > ${TEMP_FILE}

# Realizar restore
echo "Restaurando database..."
cat ${TEMP_FILE} | docker exec -i ${CONTAINER_NAME} psql -U ${DB_USER} -d ${DB_NAME}

# Limpar arquivo temporário
rm ${TEMP_FILE}

# Reiniciar aplicação
echo "Reiniciando aplicação..."
docker-compose start app1 app2 app3

echo ""
echo -e "${GREEN}Restore concluído com sucesso!${NC}"
echo ""
echo "======================================"
EOF

chmod +x scripts/restore.sh
```

**Windows (PowerShell):**
```powershell
# Similar ao backup, criar scripts/restore.ps1
# Conteúdo análogo adaptado para PowerShell
```

## Parte 4: Script de Deploy (15 min)

### 4.1 Criar script de deploy automatizado

**Linux/Mac:**
```bash
cat > scripts/deploy.sh << 'EOF'
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

# Função para log
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
    log_error "Arquivo $COMPOSE_FILE não encontrado"
    exit 1
fi

# Step 1: Backup do banco
log "Step 1/6: Criando backup do banco..."
if [ -f "scripts/backup.sh" ]; then
    ./scripts/backup.sh
    log_success "Backup criado"
else
    log_warning "Script de backup não encontrado, pulando..."
fi

# Step 2: Pull de imagens
log "Step 2/6: Baixando imagens atualizadas..."
docker-compose pull
log_success "Imagens atualizadas"

# Step 3: Build da aplicação
log "Step 3/6: Construindo aplicação..."
docker-compose build --no-cache
log_success "Build concluído"

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

# Verificar se aplicação está respondendo
HEALTH_CHECK_PASSED=false
for i in {1..10}; do
    if curl -f http://localhost/health > /dev/null 2>&1; then
        HEALTH_CHECK_PASSED=true
        break
    fi
    log "Tentativa $i/10 - Aguardando aplicação..."
    sleep 5
done

if [ "$HEALTH_CHECK_PASSED" = true ]; then
    log_success "Health check passou!"
else
    log_error "Health check falhou após 10 tentativas"
    log_warning "Executando rollback..."
    
    # Rollback: usar backup
    if [ -f "scripts/restore.sh" ]; then
        # Aqui você poderia automatizar o restore do último backup
        log_error "Por favor, execute manualmente: ./scripts/restore.sh"
    fi
    
    exit 1
fi

# Step 6: Limpeza
log "Step 6/6: Limpando recursos não utilizados..."
docker image prune -f
log_success "Limpeza concluída"

# Mostrar status final
echo ""
echo "======================================"
log_success "Deploy concluído com sucesso!"
echo "======================================"
echo ""
echo "Status dos serviços:"
docker-compose ps

echo ""
echo "Logs recentes:"
docker-compose logs --tail=5

echo ""
echo "Acesse: http://localhost"
echo ""
EOF

chmod +x scripts/deploy.sh
```

**Windows (PowerShell):**
```powershell
# Criar scripts/deploy.ps1 similar
```

## Parte 5: Configuração de Produção (10 min - Bônus)

### 5.1 Criar docker-compose.prod.yml

```yaml
version: '3.8'

services:
  nginx:
    environment:
      - NGINX_ENTRYPOINT_QUIET_LOGS=1
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 256M
        reservations:
          cpus: '0.5'
          memory: 128M

  app1:
    environment:
      - FLASK_ENV=production
      - LOG_LEVEL=info
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  app2:
    environment:
      - FLASK_ENV=production
      - LOG_LEVEL=info
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  app3:
    environment:
      - FLASK_ENV=production
      - LOG_LEVEL=info
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  db:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M

  redis:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
```

**Usar em produção:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Checklist de Validação Final

### Funcionalidades
- [ ] Health checks detalhados implementados (/health, /ready, /live)
- [ ] Logs estruturados em JSON
- [ ] Script de backup funcional
- [ ] Script de restore funcional
- [ ] Script de deploy automatizado
- [ ] docker-compose.prod.yml configurado

### Testes
- [ ] Backup realizado com sucesso
- [ ] Restore testado e funcionando
- [ ] Deploy script executado sem erros
- [ ] Health checks respondendo corretamente
- [ ] Logs sendo gerados em formato JSON
- [ ] Aplicação recupera de falhas automaticamente

### Produção Ready
- [ ] Senhas fortes no .env
- [ ] .env no .gitignore
- [ ] Resource limits configurados
- [ ] Restart policies ativas
- [ ] Volumes persistentes
- [ ] Backups automatizados (cron)

## Testar Stack Completa

```bash
# 1. Deploy completo
./scripts/deploy.sh

# 2. Criar algumas tarefas via interface

# 3. Fazer backup
./scripts/backup.sh

# 4. Simular falha
docker-compose stop app1

# 5. Verificar que continua funcionando
curl http://localhost/health

# 6. Recuperar instância
docker-compose start app1

# 7. Verificar logs
docker-compose logs --tail=50

# 8. Ver logs estruturados
cat logs/app1/app.json.log | jq '.'
```

## Próximos Passos

### Módulo 06 - Infrastructure as Code
- Provisionar VMs com Terraform
- Automatizar deployment com Ansible
- Gerenciar múltiplos ambientes

### Módulo 07 - CI/CD
- GitHub Actions / GitLab CI
- Testes automatizados
- Deploy automatizado para produção

### Módulo 08 - Observabilidade
- Prometheus + Grafana para métricas
- Loki para logs centralizados
- Alertmanager para alertas
- Dashboards customizados

## Parabéns!

Você completou o Módulo 05 de Docker Compose!

Sua aplicação agora está:
- Altamente disponível (3 instâncias)
- Com load balancing (Nginx)
- Com dados persistentes (PostgreSQL)
- Com cache (Redis)
- Com health checks robustos
- Com logs estruturados
- Com backup/restore automatizado
- Pronta para produção

**Esta é uma stack profissional que você pode usar em projetos reais!**