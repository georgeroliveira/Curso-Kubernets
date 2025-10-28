# Deploy: Estratégias de Deploy e CI/CD

## Estratégias de Deploy

### 1. Deploy Manual

#### Preparação do Ambiente
```bash
# Estrutura recomendada
/opt/taskmanager/
├── docker-compose.yml
├── docker-compose.prod.yml
├── nginx.conf
├── .env.prod
├── scripts/
│   ├── deploy.sh
│   ├── backup.sh
│   └── rollback.sh
└── backups/
```

#### Script de Deploy Manual
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

PROJECT_NAME="taskmanager"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env.prod"

echo "Iniciando deploy do TaskManager..."

# Verificar arquivos necessários
if [[ ! -f "$COMPOSE_FILE" ]]; then
    echo "ERRO: Arquivo $COMPOSE_FILE não encontrado"
    exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
    echo "ERRO: Arquivo $ENV_FILE não encontrado"
    exit 1
fi

# Backup do banco antes do deploy
echo "Criando backup do banco..."
./scripts/backup.sh

# Pull das imagens mais recentes
echo "Baixando imagens atualizadas..."
docker-compose pull

# Build da aplicação
echo "Construindo aplicação..."
docker-compose build --no-cache app

# Deploy com zero downtime
echo "Executando deploy..."
docker-compose up -d --force-recreate

# Aguardar serviços ficarem saudáveis
echo "Aguardando health checks..."
sleep 30

# Verificar se aplicação está respondendo
if curl -f http://localhost/health >/dev/null 2>&1; then
    echo "Deploy concluído com sucesso!"
    
    # Limpeza de imagens antigas
    docker image prune -f
    
    echo "Limpeza concluída"
else
    echo "ERRO: Health check falhou, executando rollback..."
    ./scripts/rollback.sh
    exit 1
fi
```

### 2. Blue-Green Deploy

#### docker-compose.blue-green.yml
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-blue-green.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - app-blue
      - app-green

  app-blue:
    build: .
    environment:
      - DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=blue
    depends_on:
      - db
      - redis

  app-green:
    build: .
    environment:
      - DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=green
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: taskdb
      POSTGRES_USER: taskuser
      POSTGRES_PASSWORD: taskpass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

#### Script Blue-Green Deploy
```bash
#!/bin/bash
# scripts/blue-green-deploy.sh

CURRENT_ENV=$(curl -s http://localhost/health | jq -r '.environment' 2>/dev/null || echo "blue")
NEW_ENV=$([ "$CURRENT_ENV" = "blue" ] && echo "green" || echo "blue")

echo "Deploy Blue-Green: $CURRENT_ENV -> $NEW_ENV"

# Build nova versão no ambiente inativo
echo "Construindo versão no ambiente $NEW_ENV..."
docker-compose -f docker-compose.blue-green.yml build app-$NEW_ENV

# Subir nova versão
echo "Subindo ambiente $NEW_ENV..."
docker-compose -f docker-compose.blue-green.yml up -d app-$NEW_ENV

# Aguardar health check
echo "Aguardando health check do ambiente $NEW_ENV..."
for i in {1..30}; do
    if docker-compose -f docker-compose.blue-green.yml exec app-$NEW_ENV curl -f http://localhost:3000/health >/dev/null 2>&1; then
        echo "Ambiente $NEW_ENV está saudável"
        break
    fi
    sleep 5
done

# Atualizar nginx para apontar para novo ambiente
echo "Redirecionando tráfego para ambiente $NEW_ENV..."
sed -i "s/server app-$CURRENT_ENV:3000;/server app-$NEW_ENV:3000;/" nginx-blue-green.conf
docker-compose -f docker-compose.blue-green.yml exec nginx nginx -s reload

# Aguardar um tempo antes de remover ambiente antigo
echo "Aguardando 60 segundos antes de remover ambiente $CURRENT_ENV..."
sleep 60

# Remover ambiente antigo
echo "Removendo ambiente $CURRENT_ENV..."
docker-compose -f docker-compose.blue-green.yml stop app-$CURRENT_ENV
docker-compose -f docker-compose.blue-green.yml rm -f app-$CURRENT_ENV

echo "Deploy Blue-Green concluído!"
```

### 3. Rolling Deploy

#### Script Rolling Deploy
```bash
#!/bin/bash
# scripts/rolling-deploy.sh

REPLICAS=3
PROJECT_NAME="taskmanager"

echo "Iniciando Rolling Deploy com $REPLICAS réplicas..."

# Build nova versão
echo "Construindo nova versão..."
docker-compose build --no-cache app

# Deploy uma réplica por vez
for i in $(seq 1 $REPLICAS); do
    echo "Atualizando réplica $i de $REPLICAS..."
    
    # Parar réplica atual
    docker-compose stop app$i
    docker-compose rm -f app$i
    
    # Subir nova réplica
    docker-compose up -d app$i
    
    # Aguardar health check
    sleep 30
    
    # Verificar se réplica está saudável
    if docker-compose exec app$i curl -f http://localhost:3000/health >/dev/null 2>&1; then
        echo "Réplica $i atualizada com sucesso"
    else
        echo "ERRO: Réplica $i falhou no health check"
        exit 1
    fi
done

echo "Rolling Deploy concluído!"
```

## Automação com CI/CD

### 1. GitHub Actions

#### .github/workflows/deploy.yml
```yaml
name: Deploy TaskManager

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
      env:
        DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb
    
    - name: Run integration tests
      run: npm run test:integration

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t taskmanager:${{ github.sha }} .
        docker tag taskmanager:${{ github.sha }} taskmanager:latest
    
    - name: Test Docker image
      run: |
        docker run -d --name test-app taskmanager:latest
        sleep 10
        docker exec test-app curl -f http://localhost:3000/health

  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /opt/taskmanager
          git pull origin main
          ./scripts/deploy.sh
```

### 2. GitLab CI

#### .gitlab-ci.yml
```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: node:18
  services:
    - postgres:15
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: testpass
    DATABASE_URL: postgresql://postgres:testpass@postgres:5432/testdb
  script:
    - npm ci
    - npm test
    - npm run test:integration

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main

deploy:
  stage: deploy
  image: alpine:latest
  before_script:
    - apk add --no-cache openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
    - mkdir -p ~/.ssh
    - chmod 700 ~/.ssh
  script:
    - ssh -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_HOST "
        cd /opt/taskmanager &&
        export DOCKER_IMAGE=$DOCKER_IMAGE &&
        ./scripts/deploy.sh"
  only:
    - main
```

## Scripts de Suporte

### 1. Script de Backup
```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="/opt/taskmanager/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/taskmanager_$DATE.sql"

echo "Iniciando backup do banco de dados..."

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Realizar backup
docker-compose exec -T db pg_dump -U taskuser taskdb > $BACKUP_FILE

# Compactar backup
gzip $BACKUP_FILE

# Manter apenas últimos 7 backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Backup realizado: ${BACKUP_FILE}.gz"
```

### 2. Script de Rollback
```bash
#!/bin/bash
# scripts/rollback.sh

BACKUP_DIR="/opt/taskmanager/backups"

echo "Iniciando rollback..."

# Listar backups disponíveis
echo "Backups disponíveis:"
ls -la $BACKUP_DIR/*.sql.gz

# Solicitar qual backup usar
read -p "Digite o nome do backup para restaurar: " BACKUP_NAME

if [[ ! -f "$BACKUP_DIR/$BACKUP_NAME" ]]; then
    echo "ERRO: Backup não encontrado"
    exit 1
fi

# Confirmar rollback
read -p "Confirma rollback para $BACKUP_NAME? (y/N): " CONFIRM
if [[ "$CONFIRM" != "y" ]]; then
    echo "Rollback cancelado"
    exit 0
fi

# Parar aplicação
echo "Parando aplicação..."
docker-compose stop app

# Restaurar banco
echo "Restaurando banco de dados..."
gunzip -c "$BACKUP_DIR/$BACKUP_NAME" | docker-compose exec -T db psql -U taskuser -d taskdb

# Reiniciar aplicação
echo "Reiniciando aplicação..."
docker-compose up -d app

# Verificar se aplicação voltou
sleep 30
if curl -f http://localhost/health >/dev/null 2>&1; then
    echo "Rollback concluído com sucesso!"
else
    echo "ERRO: Aplicação não respondeu após rollback"
    exit 1
fi
```

### 3. Script de Monitoramento
```bash
#!/bin/bash
# scripts/monitor.sh

check_service() {
    local service=$1
    local url=$2
    
    if curl -f $url >/dev/null 2>&1; then
        echo "OK: $service está respondendo"
        return 0
    else
        echo "ERRO: $service não está respondendo"
        return 1
    fi
}

echo "Verificando status dos serviços..."

# Verificar aplicação
check_service "TaskManager" "http://localhost/health"

# Verificar nginx
check_service "Nginx" "http://localhost/nginx_status"

# Verificar containers
echo "Status dos containers:"
docker-compose ps

# Verificar uso de recursos
echo "Uso de recursos:"
docker stats --no-stream

# Verificar logs recentes
echo "Logs recentes de erro:"
docker-compose logs --tail=10 | grep -i error
```

## Configuração de Ambientes

### 1. .env.production
```bash
# Banco de dados
DATABASE_URL=postgresql://taskuser:strong_password@db:5432/taskdb
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=strong_password

# Redis
REDIS_URL=redis://redis:6379

# Aplicação
NODE_ENV=production
PORT=3000
JWT_SECRET=very_strong_jwt_secret_key

# Logs
LOG_LEVEL=info
LOG_FILE=/app/logs/app.log

# Limites
MAX_REQUESTS_PER_MINUTE=100
MAX_FILE_SIZE=10mb
```

### 2. .env.staging
```bash
# Banco de dados
DATABASE_URL=postgresql://taskuser:staging_password@db:5432/taskdb_staging
POSTGRES_DB=taskdb_staging
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=staging_password

# Redis
REDIS_URL=redis://redis:6379

# Aplicação
NODE_ENV=staging
PORT=3000
JWT_SECRET=staging_jwt_secret_key

# Debug
DEBUG=true
LOG_LEVEL=debug
```

## Checklist de Deploy

### Pré-Deploy
- [ ] Testes passando
- [ ] Backup do banco realizado
- [ ] Variáveis de ambiente configuradas
- [ ] Health checks implementados
- [ ] Logs configurados

### Durante Deploy
- [ ] Monitorar logs em tempo real
- [ ] Verificar health checks
- [ ] Testar endpoints críticos
- [ ] Monitorar métricas de performance

### Pós-Deploy
- [ ] Validar funcionalidades principais
- [ ] Verificar integrações externas
- [ ] Confirmar backup automático
- [ ] Documentar alterações
- [ ] Notificar equipe

## Troubleshooting

### Problemas Comuns

1. **Container não sobe**
   ```bash
   # Verificar logs
   docker-compose logs service_name
   
   # Verificar recursos
   docker system df
   
   # Limpar cache
   docker system prune -f
   ```

2. **Banco não conecta**
   ```bash
   # Verificar rede
   docker network ls
   docker network inspect network_name
   
   # Testar conectividade
   docker-compose exec app nc -zv db 5432
   ```

3. **Deploy lento**
   ```bash
   # Verificar imagens
   docker images
   
   # Otimizar build
   docker-compose build --parallel
   
   # Usar cache
   docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1
   ```

### Recovery de Emergência

```bash
#!/bin/bash
# scripts/emergency-recovery.sh

echo "INICIANDO RECOVERY DE EMERGÊNCIA"

# Parar todos os serviços
docker-compose down

# Restaurar último backup
LATEST_BACKUP=$(ls -t /opt/taskmanager/backups/*.sql.gz | head -1)
echo "Restaurando backup: $LATEST_BACKUP"

# Subir apenas o banco
docker-compose up -d db
sleep 30

# Restaurar dados
gunzip -c $LATEST_BACKUP | docker-compose exec -T db psql -U taskuser -d taskdb

# Subir todos os serviços
docker-compose up -d

echo "Recovery concluído - verificar aplicação manualmente"
```