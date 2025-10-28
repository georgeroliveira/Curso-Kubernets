# Shell Scripts para Automação

## Por que Shell Scripts em IaC?

Shell scripts são a base da automação em Linux e servem como ponte entre comandos manuais e ferramentas mais avançadas como Ansible.

### Vantagens
- **Simplicidade**: Comandos que você já conhece
- **Rapidez**: Para automações simples
- **Universalidade**: Funciona em qualquer Linux
- **Base**: Fundamento para Ansible/Terraform

### Quando usar
- Instalação de dependências
- Scripts de inicialização
- Automação rápida
- Validações simples

---

## Estrutura de um Script

### Template Básico
```bash
#!/bin/bash
# Script: install-docker.sh
# Descrição: Instala Docker no Ubuntu
# Autor: DevOps Bootcamp
# Data: 2024

set -e  # Para na primeira falha
set -u  # Erro em variáveis não definidas

# Variáveis
DOCKER_VERSION="20.10.21"
LOG_FILE="/tmp/install-docker.log"

# Função principal
main() {
    echo "Iniciando instalação do Docker..."
    install_dependencies
    add_docker_repository
    install_docker
    configure_docker
    verify_installation
    echo "Docker instalado com sucesso!"
}

# Executar se script for chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### Boas Práticas
```bash
# Shebang sempre na primeira linha
#!/bin/bash

# Configurações de segurança
set -e          # Exit on error
set -u          # Error on undefined variables
set -o pipefail # Error on pipe failures

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função de log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}
```

---

## Scripts para TaskManager

### 1. Script de Dependências
```bash
#!/bin/bash
# install-dependencies.sh

set -e

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

install_basic_packages() {
    log "Instalando pacotes básicos..."
    sudo apt update
    sudo apt install -y \
        curl \
        wget \
        git \
        python3 \
        python3-pip \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
}

install_docker() {
    log "Verificando se Docker já está instalado..."
    if command -v docker &> /dev/null; then
        log "Docker já está instalado: $(docker --version)"
        return 0
    fi

    log "Instalando Docker..."
    
    # Adicionar chave GPG
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Adicionar repositório
    echo \
      "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Instalar Docker
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io

    # Adicionar usuário ao grupo
    sudo usermod -aG docker $USER

    log "Docker instalado com sucesso!"
}

install_docker_compose() {
    log "Verificando Docker Compose..."
    if command -v docker-compose &> /dev/null; then
        log "Docker Compose já está instalado: $(docker-compose --version)"
        return 0
    fi

    log "Instalando Docker Compose..."
    COMPOSE_VERSION="2.12.2"
    sudo curl -L "https://github.com/docker/compose/releases/download/v${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    log "Docker Compose instalado com sucesso!"
}

verify_installation() {
    log "Verificando instalação..."
    
    echo "Versões instaladas:"
    python3 --version
    git --version
    docker --version
    docker-compose --version
    
    log "Todas as dependências foram instaladas com sucesso!"
}

main() {
    log "=== Instalação de Dependências TaskManager ==="
    install_basic_packages
    install_docker
    install_docker_compose
    verify_installation
    
    echo ""
    log "IMPORTANTE: Faça logout e login novamente para usar Docker sem sudo"
}

main "$@"
```

### 2. Script de Deploy
```bash
#!/bin/bash
# deploy-taskmanager.sh

set -e

# Variáveis
PROJECT_DIR="${HOME}/taskmanager"
BACKUP_DIR="${HOME}/taskmanager-backups"
COMPOSE_FILE="docker-compose.yml"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

error() {
    echo "[ERROR] $1" >&2
    exit 1
}

check_prerequisites() {
    log "Verificando pré-requisitos..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado. Execute install-dependencies.sh primeiro"
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não está instalado"
    fi
    
    # Verificar se Docker está rodando
    if ! sudo systemctl is-active --quiet docker; then
        log "Iniciando Docker..."
        sudo systemctl start docker
    fi
    
    # Verificar projeto
    if [ ! -d "$PROJECT_DIR" ]; then
        error "Diretório $PROJECT_DIR não encontrado"
    fi
    
    if [ ! -f "$PROJECT_DIR/$COMPOSE_FILE" ]; then
        error "Arquivo $COMPOSE_FILE não encontrado em $PROJECT_DIR"
    fi
    
    log "Pré-requisitos OK!"
}

backup_current_state() {
    log "Fazendo backup do estado atual..."
    
    mkdir -p "$BACKUP_DIR"
    BACKUP_FILE="$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).tar.gz"
    
    cd "$PROJECT_DIR"
    
    # Backup de dados se existirem
    if docker-compose ps | grep -q "Up"; then
        log "Fazendo backup dos dados do banco..."
        docker-compose exec -T db pg_dump -U taskuser taskdb > "$BACKUP_DIR/db-backup-$(date +%Y%m%d-%H%M%S).sql" || true
    fi
    
    # Backup de configurações
    tar -czf "$BACKUP_FILE" --exclude='*.log' --exclude='__pycache__' .
    
    log "Backup salvo em: $BACKUP_FILE"
}

pull_latest_code() {
    log "Atualizando código..."
    
    cd "$PROJECT_DIR"
    
    # Se for um repositório Git
    if [ -d ".git" ]; then
        git fetch origin
        git pull origin main
    else
        log "Não é um repositório Git, pulando atualização"
    fi
}

deploy_application() {
    log "Fazendo deploy da aplicação..."
    
    cd "$PROJECT_DIR"
    
    # Parar containers atuais
    log "Parando containers existentes..."
    docker-compose down || true
    
    # Pull de imagens
    log "Baixando imagens atualizadas..."
    docker-compose pull
    
    # Build da aplicação
    log "Construindo aplicação..."
    docker-compose build --no-cache
    
    # Subir stack
    log "Subindo stack TaskManager..."
    docker-compose up -d
    
    # Aguardar aplicação
    log "Aguardando aplicação ficar pronta..."
    sleep 30
}

verify_deployment() {
    log "Verificando deploy..."
    
    # Verificar containers
    if ! docker-compose ps | grep -q "Up"; then
        error "Containers não estão rodando"
    fi
    
    # Verificar health check
    local max_attempts=12
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost/health >/dev/null 2>&1; then
            log "Health check passou!"
            break
        fi
        
        log "Tentativa $attempt/$max_attempts - aguardando aplicação..."
        sleep 10
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        error "Health check falhou após $max_attempts tentativas"
    fi
    
    # Verificar endpoints principais
    if curl -f http://localhost/ >/dev/null 2>&1; then
        log "Aplicação principal respondendo"
    else
        log "WARNING: Aplicação principal não responde"
    fi
    
    log "Deploy verificado com sucesso!"
}

show_status() {
    log "=== Status Final ==="
    echo ""
    echo "Containers rodando:"
    docker-compose ps
    echo ""
    echo "URLs disponíveis:"
    echo "  - Aplicação: http://localhost/"
    echo "  - Health check: http://localhost/health"
    echo ""
    log "Deploy concluído com sucesso!"
}

main() {
    log "=== Deploy TaskManager ==="
    
    check_prerequisites
    backup_current_state
    pull_latest_code
    deploy_application
    verify_deployment
    show_status
}

# Trap para limpeza em caso de erro
trap 'error "Deploy falhou! Verifique os logs com: docker-compose logs"' ERR

main "$@"
```

### 3. Script de Ambiente
```bash
#!/bin/bash
# setup-environment.sh

set -e

# Configurações
PROJECT_NAME="taskmanager"
PROJECT_DIR="${HOME}/${PROJECT_NAME}"
REPO_URL="https://github.com/SEU_USUARIO/taskmanager-devops.git"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

setup_directories() {
    log "Criando estrutura de diretórios..."
    
    mkdir -p "${PROJECT_DIR}"/{logs,backups,scripts}
    mkdir -p "${HOME}/.local/bin"
    
    log "Diretórios criados em: $PROJECT_DIR"
}

clone_or_update_project() {
    log "Configurando projeto TaskManager..."
    
    if [ -d "$PROJECT_DIR/.git" ]; then
        log "Projeto já existe, atualizando..."
        cd "$PROJECT_DIR"
        git pull origin main
    else
        log "Clonando projeto..."
        if [ -n "$REPO_URL" ]; then
            git clone "$REPO_URL" "$PROJECT_DIR"
        else
            log "URL do repositório não configurada, criando estrutura básica..."
            cd "$PROJECT_DIR"
            git init
        fi
    fi
}

setup_environment_file() {
    log "Configurando arquivo de ambiente..."
    
    cat > "$PROJECT_DIR/.env" << EOF
# TaskManager Environment Configuration
FLASK_ENV=production
DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb
REDIS_URL=redis://redis:6379

# PostgreSQL
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpass

# Logs
LOG_LEVEL=info
EOF

    log "Arquivo .env criado"
}

setup_compose_file() {
    if [ ! -f "$PROJECT_DIR/docker-compose.yml" ]; then
        log "Criando docker-compose.yml..."
        
        cat > "$PROJECT_DIR/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb
      - REDIS_URL=redis://redis:6379
      - FLASK_ENV=production
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: taskdb
      POSTGRES_USER: taskuser
      POSTGRES_PASSWORD: taskpass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
EOF
        
        log "docker-compose.yml criado"
    else
        log "docker-compose.yml já existe"
    fi
}

setup_nginx_config() {
    if [ ! -f "$PROJECT_DIR/nginx.conf" ]; then
        log "Criando configuração Nginx..."
        
        cat > "$PROJECT_DIR/nginx.conf" << 'EOF'
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        access_log off;
        return 200 "healthy from nginx\n";
    }

    # Cache arquivos estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
        
        log "nginx.conf criado"
    else
        log "nginx.conf já existe"
    fi
}

configure_git() {
    log "Configurando Git..."
    
    # Verificar se Git está configurado
    if ! git config --global user.name >/dev/null 2>&1; then
        log "Configurando usuário Git..."
        git config --global user.name "TaskManager User"
        git config --global user.email "user@taskmanager.local"
    fi
    
    # Configurar .gitignore se não existir
    if [ ! -f "$PROJECT_DIR/.gitignore" ]; then
        cat > "$PROJECT_DIR/.gitignore" << 'EOF'
# Environment
.env
.env.local

# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Docker
.dockerignore

# Backups
backups/
EOF
        log ".gitignore criado"
    fi
}

create_helper_scripts() {
    log "Criando scripts auxiliares..."
    
    # Script de start
    cat > "$PROJECT_DIR/start.sh" << 'EOF'
#!/bin/bash
echo "Iniciando TaskManager..."
docker-compose up -d
echo "TaskManager iniciado! Acesse: http://localhost"
EOF
    
    # Script de stop
    cat > "$PROJECT_DIR/stop.sh" << 'EOF'
#!/bin/bash
echo "Parando TaskManager..."
docker-compose down
echo "TaskManager parado!"
EOF
    
    # Script de logs
    cat > "$PROJECT_DIR/logs.sh" << 'EOF'
#!/bin/bash
echo "Logs do TaskManager:"
docker-compose logs -f
EOF
    
    # Tornar executáveis
    chmod +x "$PROJECT_DIR"/{start.sh,stop.sh,logs.sh}
    
    log "Scripts auxiliares criados"
}

show_summary() {
    log "=== Resumo da Configuração ==="
    echo ""
    echo "Projeto criado em: $PROJECT_DIR"
    echo ""
    echo "Para usar:"
    echo "  cd $PROJECT_DIR"
    echo "  ./start.sh     # Iniciar"
    echo "  ./stop.sh      # Parar"
    echo "  ./logs.sh      # Ver logs"
    echo ""
    echo "URLs:"
    echo "  - Aplicação: http://localhost/"
    echo "  - Health: http://localhost/health"
    echo ""
    log "Ambiente configurado com sucesso!"
}

main() {
    log "=== Configuração do Ambiente TaskManager ==="
    
    setup_directories
    clone_or_update_project
    setup_environment_file
    setup_compose_file
    setup_nginx_config
    configure_git
    create_helper_scripts
    show_summary
}

main "$@"
```

---

## Técnicas Avançadas

### 1. Tratamento de Erros
```bash
# Função de cleanup
cleanup() {
    echo "Limpando recursos..."
    docker-compose down || true
    rm -f /tmp/deploy.lock
}

# Registrar cleanup para execução ao sair
trap cleanup EXIT

# Tratamento específico de erros
handle_error() {
    local exit_code=$1
    local line_number=$2
    echo "ERRO na linha $line_number (código: $exit_code)"
    cleanup
    exit $exit_code
}

trap 'handle_error $? $LINENO' ERR
```

### 2. Validações
```bash
validate_environment() {
    local errors=0
    
    # Verificar sistema operacional
    if [[ ! "$(lsb_release -si)" == "Ubuntu" ]]; then
        error "Este script é para Ubuntu apenas"
        ((errors++))
    fi
    
    # Verificar versão Ubuntu
    local version=$(lsb_release -rs)
    if [[ $(echo "$version < 20.04" | bc) -eq 1 ]]; then
        warning "Ubuntu $version pode ter problemas. Recomendado: 20.04+"
    fi
    
    # Verificar espaço em disco
    local available_space=$(df / | awk 'NR==2 {print $4}')
    if [[ $available_space -lt 2097152 ]]; then  # 2GB
        error "Espaço insuficiente. Necessário: 2GB, Disponível: $(($available_space/1048576))GB"
        ((errors++))
    fi
    
    # Verificar memória
    local available_memory=$(free -m | awk 'NR==2{print $7}')
    if [[ $available_memory -lt 1024 ]]; then  # 1GB
        warning "Memória baixa: ${available_memory}MB. Recomendado: 1GB+"
    fi
    
    if [[ $errors -gt 0 ]]; then
        error "Validação falhou com $errors erro(s)"
    fi
    
    log "Validação do ambiente passou!"
}
```

### 3. Logging Avançado
```bash
# Configurar logging
setup_logging() {
    local log_dir="${PROJECT_DIR}/logs"
    local log_file="${log_dir}/deploy-$(date +%Y%m%d-%H%M%S).log"
    
    mkdir -p "$log_dir"
    
    # Redirecionar stdout e stderr para arquivo e terminal
    exec 1> >(tee -a "$log_file")
    exec 2> >(tee -a "$log_file" >&2)
    
    log "Logging configurado: $log_file"
}
```

---

## Integração com Ansible

### Scripts como base para Playbooks
```yaml
# playbook.yml
- name: Executar script de instalação
  script: scripts/install-dependencies.sh
  
- name: Executar script customizado
  shell: |
    {{ lookup('file', 'scripts/custom-setup.sh') }}
```

### Validação de Scripts
```bash
# validate-scripts.sh
#!/bin/bash

echo "Validando scripts Shell..."

# ShellCheck para sintaxe
for script in scripts/*.sh; do
    echo "Validando: $script"
    shellcheck "$script"
done

# Teste básico de execução
bash -n scripts/install-dependencies.sh

echo "Validação concluída!"
```

---

## Próximos Passos

Os scripts Shell criados neste módulo serão:
1. **Executados manualmente** para entender automação
2. **Integrados no Ansible** para orquestração completa
3. **Validados no pipeline** para garantir qualidade

No próximo tópico veremos como o Ansible usa esses conceitos de forma mais robusta e idempotente.