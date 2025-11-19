# Lab 01 - Stack Multi-Container

**Duração:** 60 minutos  
**Dificuldade:** Iniciante/Intermediário

## Objetivos

Ao final deste lab você será capaz de:
- Criar e gerenciar múltiplos containers com Docker Compose
- Configurar PostgreSQL como banco de dados
- Implementar Redis para cache
- Conectar serviços através de redes Docker
- Persistir dados com volumes

## Pré-requisitos

- Docker e Docker Compose instalados
- Código do TaskManager do Módulo 04
- Editor de texto (VS Code, Nano, Vim, Notepad++)

## Parte 1: Preparação do Ambiente (10 min)

### 1.1 Criar estrutura de pastas

**Linux/Mac:**
```bash
# Criar pasta do módulo
mkdir -p ~/devops-course/modulo-05-compose
cd ~/devops-course/modulo-05-compose

# Copiar código do TaskManager
cp -r ~/devops-course/modulo-04-docker/taskmanager .

# Criar pastas adicionais
mkdir -p config scripts data logs

# Verificar estrutura
ls -la
```

**Windows (PowerShell):**
```powershell
# Criar pasta do módulo
New-Item -Path "$HOME\devops-course\modulo-05-compose" -ItemType Directory -Force
Set-Location "$HOME\devops-course\modulo-05-compose"

# Copiar código do TaskManager
Copy-Item -Path "..\modulo-04-docker\taskmanager" -Destination "." -Recurse

# Criar pastas adicionais
New-Item -Path "config" -ItemType Directory -Force
New-Item -Path "scripts" -ItemType Directory -Force
New-Item -Path "data" -ItemType Directory -Force
New-Item -Path "logs" -ItemType Directory -Force

# Verificar estrutura
Get-ChildItem
```

**Estrutura esperada:**
```
modulo-05-compose/
├── taskmanager/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── templates/
├── config/
├── scripts/
├── data/
└── logs/
```

### 1.2 Criar arquivo .env

**Linux/Mac:**
```bash
cat > .env << 'EOF'
# Database Configuration
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpass123

# Application Configuration
FLASK_ENV=production
SECRET_KEY=change-this-in-production-please

# Ports
APP_PORT=5000
DB_PORT=5432
REDIS_PORT=6379
EOF
```

**Windows (PowerShell):**
```powershell
@"
# Database Configuration
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpass123

# Application Configuration
FLASK_ENV=production
SECRET_KEY=change-this-in-production-please

# Ports
APP_PORT=5000
DB_PORT=5432
REDIS_PORT=6379
"@ | Out-File -FilePath .env -Encoding UTF8
```

**IMPORTANTE:** Adicione `.env` ao `.gitignore`:

**Linux/Mac:**
```bash
echo ".env" >> .gitignore
echo "data/" >> .gitignore
echo "logs/" >> .gitignore
```

**Windows (PowerShell):**
```powershell
Add-Content -Path .gitignore -Value ".env"
Add-Content -Path .gitignore -Value "data/"
Add-Content -Path .gitignore -Value "logs/"
```

## Parte 2: Configurar PostgreSQL (15 min)

### 2.1 Criar script de inicialização do banco

**Linux/Mac:**
```bash
cat > config/init.sql << 'EOF'
-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de tarefas
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC);

-- Inserir usuário padrão (senha: admin123)
INSERT INTO users (username, email, password_hash) 
VALUES ('admin', 'admin@taskmanager.local', 'pbkdf2:sha256:260000$salt$hash')
ON CONFLICT (username) DO NOTHING;

-- Inserir tarefas de exemplo
INSERT INTO tasks (user_id, title, description, completed) 
VALUES 
    (1, 'Configurar Docker Compose', 'Aprender orquestração multi-container', false),
    (1, 'Adicionar PostgreSQL', 'Migrar dados para banco relacional', true),
    (1, 'Implementar Redis', 'Adicionar cache para performance', false),
    (1, 'Configurar Nginx', 'Setup de proxy reverso', false)
ON CONFLICT DO NOTHING;

-- Log de inicialização
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully!';
END $$;
EOF
```

**Windows (PowerShell):**
```powershell
@"
-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de tarefas
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC);

-- Inserir usuário padrão (senha: admin123)
INSERT INTO users (username, email, password_hash) 
VALUES ('admin', 'admin@taskmanager.local', 'pbkdf2:sha256:260000$salt$hash')
ON CONFLICT (username) DO NOTHING;

-- Inserir tarefas de exemplo
INSERT INTO tasks (user_id, title, description, completed) 
VALUES 
    (1, 'Configurar Docker Compose', 'Aprender orquestração multi-container', false),
    (1, 'Adicionar PostgreSQL', 'Migrar dados para banco relacional', true),
    (1, 'Implementar Redis', 'Adicionar cache para performance', false),
    (1, 'Configurar Nginx', 'Setup de proxy reverso', false)
ON CONFLICT DO NOTHING;

-- Log de inicialização
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully!';
END $$;
"@ | Out-File -FilePath config/init.sql -Encoding UTF8
```

### 2.2 Atualizar requirements.txt

**Linux/Mac:**
```bash
cat > taskmanager/requirements.txt << 'EOF'
Flask==2.3.3
psycopg2-binary==2.9.7
redis==4.6.0
python-dotenv==1.0.0
Werkzeug==2.3.7
EOF
```

**Windows (PowerShell):**
```powershell
@"
Flask==2.3.3
psycopg2-binary==2.9.7
redis==4.6.0
python-dotenv==1.0.0
Werkzeug==2.3.7
"@ | Out-File -FilePath taskmanager/requirements.txt -Encoding UTF8
```

## Parte 3: Criar docker-compose.yml (20 min)

### 3.1 Arquivo docker-compose.yml completo

**Linux/Mac e Windows (mesmo conteúdo):**
```bash
# Linux/Mac
cat > docker-compose.yml << 'EOF'
# Windows PowerShell - use o editor de texto ou:
# @"
# ... conteúdo ...
# "@ | Out-File -FilePath docker-compose.yml -Encoding UTF8
```

**Conteúdo do docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Aplicação Flask
  app:
    build:
      context: ./taskmanager
      dockerfile: Dockerfile
    container_name: taskmanager-app
    ports:
      - "${APP_PORT:-5000}:5000"
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://redis:6379/0
      - FLASK_ENV=${FLASK_ENV:-production}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Banco de Dados PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: taskmanager-db
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - PGDATA=/var/lib/postgresql/data/pgdata
    ports:
      - "${DB_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./config/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  # Cache Redis
  redis:
    image: redis:7-alpine
    container_name: taskmanager-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-redis123}
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

# Volumes nomeados para persistência
volumes:
  postgres_data:
    driver: local
    name: taskmanager_postgres_data
  
  redis_data:
    driver: local
    name: taskmanager_redis_data

# Redes isoladas
networks:
  frontend:
    driver: bridge
    name: taskmanager_frontend
  
  backend:
    driver: bridge
    name: taskmanager_backend
    internal: false  # Permite acesso externo para desenvolvimento
```

### 3.2 Entendendo o docker-compose.yml

**Services (Serviços):**
- `app`: Aplicação Flask TaskManager
- `db`: Banco de dados PostgreSQL
- `redis`: Cache e sessões

**Depends_on + Health checks:**
```yaml
depends_on:
  db:
    condition: service_healthy  # Aguarda db estar saudável
```

**Networks:**
- `frontend`: App exposta para internet
- `backend`: Comunicação interna (app <-> db <-> redis)

**Volumes:**
- `postgres_data`: Dados do PostgreSQL
- `redis_data`: Persistência do Redis
- `./logs`: Bind mount para logs
- `./config/init.sql`: Script de inicialização

## Parte 4: Atualizar Aplicação (10 min)

### 4.1 Atualizar app.py com PostgreSQL e Redis

**Criar novo app.py:**

```python
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import redis
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configuração do banco
DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

# Conexão Redis
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    print("Redis connected successfully!")
except Exception as e:
    print(f"Redis connection failed: {e}")
    redis_client = None

def get_db():
    """Retorna conexão com o banco"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

@app.route('/health')
def health():
    """Health check endpoint"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {}
    }
    
    # Check PostgreSQL
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        health_status['services']['database'] = 'connected'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['services']['database'] = f'error: {str(e)}'
    
    # Check Redis
    try:
        if redis_client:
            redis_client.ping()
            health_status['services']['redis'] = 'connected'
        else:
            health_status['services']['redis'] = 'not configured'
    except Exception as e:
        health_status['services']['redis'] = f'error: {str(e)}'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

@app.route('/')
def index():
    """Página principal com cache"""
    user_id = 1  # Simplificado - em produção viria da sessão
    
    # Tentar buscar do cache
    cache_key = f"tasks:user:{user_id}"
    if redis_client:
        try:
            cached_tasks = redis_client.get(cache_key)
            if cached_tasks:
                tasks = json.loads(cached_tasks)
                print("Tasks loaded from cache")
                return render_template('index.html', tasks=tasks, from_cache=True)
        except Exception as e:
            print(f"Cache error: {e}")
    
    # Buscar do banco
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, title, description, completed, created_at 
            FROM tasks 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        ''', (user_id,))
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        
        # Salvar no cache por 5 minutos
        if redis_client:
            try:
                redis_client.setex(cache_key, 300, json.dumps(tasks, default=str))
                print("Tasks saved to cache")
            except Exception as e:
                print(f"Cache save error: {e}")
        
        return render_template('index.html', tasks=tasks, from_cache=False)
    except Exception as e:
        print(f"Database error: {e}")
        return f"Error loading tasks: {e}", 500

@app.route('/add', methods=['POST'])
def add_task():
    """Adicionar nova tarefa"""
    user_id = 1  # Simplificado
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    if not title:
        return redirect(url_for('index'))
    
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO tasks (user_id, title, description, completed)
            VALUES (%s, %s, %s, %s)
        ''', (user_id, title, description, False))
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidar cache
        if redis_client:
            cache_key = f"tasks:user:{user_id}"
            redis_client.delete(cache_key)
            print("Cache invalidated")
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error adding task: {e}")
        return f"Error: {e}", 500

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """Marcar tarefa como completa"""
    user_id = 1
    
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            UPDATE tasks 
            SET completed = NOT completed, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
        ''', (task_id, user_id))
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidar cache
        if redis_client:
            cache_key = f"tasks:user:{user_id}"
            redis_client.delete(cache_key)
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error updating task: {e}")
        return f"Error: {e}", 500

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Deletar tarefa"""
    user_id = 1
    
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, user_id))
        conn.commit()
        cur.close()
        conn.close()
        
        # Invalidar cache
        if redis_client:
            cache_key = f"tasks:user:{user_id}"
            redis_client.delete(cache_key)
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error deleting task: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### 4.2 Atualizar Dockerfile

```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório da aplicação
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios para logs e data
RUN mkdir -p /app/logs /app/data

# Expor porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando para rodar aplicação
CMD ["python", "app.py"]
```

## Parte 5: Testar a Stack (5 min)

### 5.1 Subir os serviços

**Linux/Mac:**
```bash
# Subir em background
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f
```

**Windows (PowerShell):**
```powershell
# Subir em background
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f
```

### 5.2 Verificar status

```bash
# Ver todos os containers
docker-compose ps

# Verificar health checks
docker-compose ps

# Ver logs específicos
docker-compose logs app
docker-compose logs db
docker-compose logs redis
```

**Saída esperada:**
```
NAME                 COMMAND                  SERVICE   STATUS         PORTS
taskmanager-app      "python app.py"          app       Up (healthy)   0.0.0.0:5000->5000/tcp
taskmanager-db       "docker-entrypoint.s…"   db        Up (healthy)   0.0.0.0:5432->5432/tcp
taskmanager-redis    "redis-server --appen…"  redis     Up (healthy)   0.0.0.0:6379->6379/tcp
```

### 5.3 Testar aplicação

**Abrir no navegador:**
```
http://localhost:5000
```

**Testar health check:**

**Linux/Mac:**
```bash
curl http://localhost:5000/health
```

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri http://localhost:5000/health | Select-Object -ExpandProperty Content
```

**Saída esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-13T10:30:00",
  "services": {
    "database": "connected",
    "redis": "connected"
  }
}
```

### 5.4 Testar conectividade entre containers

```bash
# Acessar container da app
docker-compose exec app sh

# Dentro do container, testar conexão com PostgreSQL
nc -zv db 5432

# Testar conexão com Redis
nc -zv redis 6379

# Sair do container
exit
```

### 5.5 Verificar dados no PostgreSQL

```bash
# Conectar no banco
docker-compose exec db psql -U taskuser -d taskdb

# Dentro do psql, executar:
\dt                           # Listar tabelas
SELECT * FROM tasks;          # Ver tarefas
SELECT * FROM users;          # Ver usuários
\q                            # Sair
```

### 5.6 Verificar cache no Redis

```bash
# Conectar no Redis
docker-compose exec redis redis-cli

# Dentro do redis-cli:
KEYS *                        # Ver todas as chaves
GET tasks:user:1              # Ver cache de tarefas
TTL tasks:user:1              # Ver tempo restante de cache
exit
```

## Checklist de Validação

- [ ] docker-compose.yml criado
- [ ] Arquivo .env configurado
- [ ] Script init.sql criado
- [ ] app.py atualizado com PostgreSQL e Redis
- [ ] requirements.txt atualizado
- [ ] Dockerfile atualizado
- [ ] Todos os containers rodando (docker-compose ps)
- [ ] Health checks passando
- [ ] Aplicação acessível em http://localhost:5000
- [ ] Pode criar, editar e deletar tarefas
- [ ] Dados persistem após restart
- [ ] Cache funcionando (verificar logs)

## Troubleshooting

### Problema: Container não sobe

```bash
# Ver logs detalhados
docker-compose logs app

# Verificar se porta está em uso
# Linux/Mac:
lsof -i :5000
# Windows PowerShell:
Get-NetTCPConnection -LocalPort 5000

# Rebuild forçado
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Não conecta no PostgreSQL

```bash
# Verificar se banco está rodando
docker-compose ps db

# Ver logs do banco
docker-compose logs db

# Testar conexão manualmente
docker-compose exec app sh
nc -zv db 5432
```

### Problema: Redis não conecta

```bash
# Verificar se Redis está rodando
docker-compose ps redis

# Ver logs do Redis
docker-compose logs redis

# Testar conexão
docker-compose exec redis redis-cli ping
```

### Problema: Dados não persistem

```bash
# Verificar volumes
docker volume ls

# Ver detalhes do volume
docker volume inspect taskmanager_postgres_data

# Se necessário, remover e recriar
docker-compose down -v
docker-compose up -d
```

## Próximos Passos

No **Lab 02** você vai:
- Adicionar Nginx como proxy reverso
- Configurar load balancer
- Escalar aplicação para 3 instâncias
- Implementar redes isoladas

**Parabéns!** Você criou sua primeira stack multi-container!