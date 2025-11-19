# Lab 02 - Nginx e Escalabilidade

**Duração:** 70 minutos  
**Dificuldade:** Intermediário

## Objetivos

Ao final deste lab você será capaz de:
- Configurar Nginx como proxy reverso
- Implementar load balancing entre múltiplas instâncias
- Escalar aplicação horizontalmente
- Configurar redes isoladas (frontend/backend)
- Implementar compressão e cache no Nginx
- Testar alta disponibilidade

## Pré-requisitos

- Lab 01 concluído e funcionando
- Stack multi-container rodando (app + db + redis)
- Conhecimento básico de Nginx

## Parte 1: Configurar Nginx (20 min)

### 1.1 Criar arquivo de configuração do Nginx

**Linux/Mac:**
```bash
# Criar pasta nginx se não existir
mkdir -p nginx

# Criar arquivo de configuração
cat > nginx/nginx.conf << 'EOF'
upstream taskmanager_backend {
    # Load balancing com round-robin (padrão)
    # least_conn;  # Descomente para usar least connections
    # ip_hash;     # Descomente para sticky sessions
    
    server app1:5000 max_fails=3 fail_timeout=30s;
    server app2:5000 max_fails=3 fail_timeout=30s;
    server app3:5000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name localhost;
    
    # Logs
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log warn;
    
    # Client body size (uploads)
    client_max_body_size 10M;
    
    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    
    # Compressão Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;
    
    # Health check endpoint do Nginx
    location /nginx-health {
        access_log off;
        return 200 "Nginx is healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Proxy para aplicação
    location / {
        proxy_pass http://taskmanager_backend;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (se necessário no futuro)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
    }
    
    # Cache de arquivos estáticos (se houver)
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://taskmanager_backend;
        proxy_cache_valid 200 1d;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
    
    # Status do Nginx (opcional - comentado por segurança)
    # location /nginx-status {
    #     stub_status on;
    #     access_log off;
    #     allow 127.0.0.1;
    #     deny all;
    # }
}
EOF
```

**Windows (PowerShell):**
```powershell
# Criar pasta nginx se não existir
New-Item -Path "nginx" -ItemType Directory -Force

# Criar arquivo de configuração
@"
upstream taskmanager_backend {
    # Load balancing com round-robin (padrão)
    # least_conn;  # Descomente para usar least connections
    # ip_hash;     # Descomente para sticky sessions
    
    server app1:5000 max_fails=3 fail_timeout=30s;
    server app2:5000 max_fails=3 fail_timeout=30s;
    server app3:5000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name localhost;
    
    # Logs
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log warn;
    
    # Client body size (uploads)
    client_max_body_size 10M;
    
    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    
    # Compressão Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;
    
    # Health check endpoint do Nginx
    location /nginx-health {
        access_log off;
        return 200 "Nginx is healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Proxy para aplicação
    location / {
        proxy_pass http://taskmanager_backend;
        
        # Headers
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
        proxy_set_header X-Forwarded-For `$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto `$scheme;
        
        # WebSocket support (se necessário no futuro)
        proxy_http_version 1.1;
        proxy_set_header Upgrade `$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
    }
    
    # Cache de arquivos estáticos (se houver)
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://taskmanager_backend;
        proxy_cache_valid 200 1d;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
    
    # Status do Nginx (opcional - comentado por segurança)
    # location /nginx-status {
    #     stub_status on;
    #     access_log off;
    #     allow 127.0.0.1;
    #     deny all;
    # }
}
"@ | Out-File -FilePath nginx/nginx.conf -Encoding UTF8
```

### 1.2 Entender a configuração do Nginx

**Upstream (Load Balancer):**
```nginx
upstream taskmanager_backend {
    server app1:5000;  # Instância 1
    server app2:5000;  # Instância 2
    server app3:5000;  # Instância 3
}
```

**Algoritmos de Load Balancing:**
- `round-robin` (padrão): Distribui requisições igualmente
- `least_conn`: Envia para servidor com menos conexões
- `ip_hash`: Mantém cliente no mesmo servidor (sticky sessions)

**Proxy Headers:**
```nginx
proxy_set_header X-Real-IP $remote_addr;           # IP real do cliente
proxy_set_header X-Forwarded-For $proxy_add_x...;  # Chain de proxies
```

**Health Checks:**
```nginx
max_fails=3 fail_timeout=30s  # Após 3 falhas, remove por 30s
```

## Parte 2: Atualizar docker-compose.yml (15 min)

### 2.1 Modificar docker-compose.yml para múltiplas instâncias

**Backup do arquivo atual:**

**Linux/Mac:**
```bash
cp docker-compose.yml docker-compose.yml.backup
```

**Windows (PowerShell):**
```powershell
Copy-Item docker-compose.yml docker-compose.yml.backup
```

**Novo docker-compose.yml:**

```yaml
version: '3.8'

services:
  # Nginx - Proxy Reverso e Load Balancer
  nginx:
    image: nginx:alpine
    container_name: taskmanager-nginx
    ports:
      - "80:80"
      - "443:443"  # Para HTTPS futuro
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - app1
      - app2
      - app3
    restart: unless-stopped
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/nginx-health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  # Aplicação Flask - Instância 1
  app1:
    build:
      context: ./taskmanager
      dockerfile: Dockerfile
    container_name: taskmanager-app1
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD:-redis123}@redis:6379/0
      - FLASK_ENV=${FLASK_ENV:-production}
      - SECRET_KEY=${SECRET_KEY}
      - INSTANCE_ID=app1
      - INSTANCE_NAME=TaskManager-Instance-1
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./logs/app1:/app/logs
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

  # Aplicação Flask - Instância 2
  app2:
    build:
      context: ./taskmanager
      dockerfile: Dockerfile
    container_name: taskmanager-app2
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD:-redis123}@redis:6379/0
      - FLASK_ENV=${FLASK_ENV:-production}
      - SECRET_KEY=${SECRET_KEY}
      - INSTANCE_ID=app2
      - INSTANCE_NAME=TaskManager-Instance-2
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./logs/app2:/app/logs
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

  # Aplicação Flask - Instância 3
  app3:
    build:
      context: ./taskmanager
      dockerfile: Dockerfile
    container_name: taskmanager-app3
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD:-redis123}@redis:6379/0
      - FLASK_ENV=${FLASK_ENV:-production}
      - SECRET_KEY=${SECRET_KEY}
      - INSTANCE_ID=app3
      - INSTANCE_NAME=TaskManager-Instance-3
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./logs/app3:/app/logs
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
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
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
  # Rede frontend - Nginx e Apps
  frontend:
    driver: bridge
    name: taskmanager_frontend
  
  # Rede backend - Apps, DB e Redis (sem acesso externo direto)
  backend:
    driver: bridge
    name: taskmanager_backend
```

### 2.2 Atualizar .env com nova variável

**Linux/Mac:**
```bash
# Adicionar senha do Redis
echo "REDIS_PASSWORD=redis123" >> .env
```

**Windows (PowerShell):**
```powershell
Add-Content -Path .env -Value "REDIS_PASSWORD=redis123"
```

### 2.3 Atualizar app.py para mostrar instância

**Modificar a função health() no app.py:**

```python
import os

@app.route('/health')
def health():
    """Health check endpoint"""
    instance_id = os.getenv('INSTANCE_ID', 'unknown')
    instance_name = os.getenv('INSTANCE_NAME', 'Unknown Instance')
    
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'instance': {
            'id': instance_id,
            'name': instance_name
        },
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
```

## Parte 3: Deploy e Teste (20 min)

### 3.1 Parar stack antiga e subir nova

**Linux/Mac:**
```bash
# Parar containers antigos
docker-compose down

# Rebuild das imagens
docker-compose build --no-cache

# Subir nova stack
docker-compose up -d

# Ver logs
docker-compose logs -f
```

**Windows (PowerShell):**
```powershell
# Parar containers antigos
docker-compose down

# Rebuild das imagens
docker-compose build --no-cache

# Subir nova stack
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 3.2 Verificar status da stack

```bash
# Ver todos os containers
docker-compose ps

# Deve mostrar 6 containers rodando:
# - nginx
# - app1, app2, app3
# - db
# - redis
```

**Saída esperada:**
```
NAME                 STATUS         PORTS
taskmanager-nginx    Up (healthy)   0.0.0.0:80->80/tcp
taskmanager-app1     Up (healthy)   
taskmanager-app2     Up (healthy)   
taskmanager-app3     Up (healthy)   
taskmanager-db       Up (healthy)   
taskmanager-redis    Up (healthy)   
```

### 3.3 Testar load balancing

**Linux/Mac:**
```bash
# Fazer várias requisições e ver qual instância responde
for i in {1..10}; do
  curl -s http://localhost/health | grep -o '"id":"app[0-9]"'
done
```

**Windows (PowerShell):**
```powershell
# Fazer várias requisições e ver qual instância responde
1..10 | ForEach-Object {
  $response = Invoke-RestMethod -Uri http://localhost/health
  Write-Host "Instance: $($response.instance.id)"
}
```

**Saída esperada (round-robin):**
```
Instance: app1
Instance: app2
Instance: app3
Instance: app1
Instance: app2
Instance: app3
...
```

### 3.4 Testar alta disponibilidade

**Parar uma instância e verificar se continua funcionando:**

```bash
# Parar app1
docker-compose stop app1

# Fazer requisições - deve funcionar com app2 e app3
curl http://localhost/health

# Verificar distribuição
# Linux/Mac:
for i in {1..6}; do
  curl -s http://localhost/health | grep -o '"id":"app[0-9]"'
done

# Windows PowerShell:
1..6 | ForEach-Object {
  $response = Invoke-RestMethod -Uri http://localhost/health
  Write-Host "Instance: $($response.instance.id)"
}

# Subir app1 novamente
docker-compose start app1
```

### 3.5 Testar no navegador

**Abrir navegador:**
```
http://localhost
```

**Teste:**
1. Criar várias tarefas
2. Abrir DevTools (F12) > Network
3. Ver header `X-Forwarded-For` nas requisições
4. Recarregar página várias vezes
5. Ver logs do Nginx para conferir distribuição

### 3.6 Ver logs do Nginx

**Linux/Mac:**
```bash
# Logs em tempo real
docker-compose logs -f nginx

# Ver access log
tail -f logs/nginx/access.log

# Ver error log
tail -f logs/nginx/error.log
```

**Windows (PowerShell):**
```powershell
# Logs em tempo real
docker-compose logs -f nginx

# Ver access log
Get-Content logs/nginx/access.log -Wait -Tail 20

# Ver error log
Get-Content logs/nginx/error.log -Wait -Tail 20
```

## Parte 4: Escalar Dinamicamente (10 min)

### 4.1 Adicionar mais instâncias via scale

**NOTA:** O `docker-compose scale` não funciona bem com containers nomeados. Vamos criar uma versão sem `container_name` para escalar.

**Criar docker-compose.scale.yml:**

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
    networks:
      - frontend

  app:
    build: ./taskmanager
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://:${REDIS_PASSWORD:-redis123}@redis:6379/0
      - FLASK_ENV=${FLASK_ENV:-production}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    networks:
      - frontend
      - backend

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./config/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  postgres_data:
  redis_data:

networks:
  frontend:
  backend:
```

**Atualizar nginx.conf para scale:**

```nginx
upstream taskmanager_backend {
    # DNS resolver para descobrir containers dinamicamente
    server app:5000;
}
```

**Escalar para 5 instâncias:**

```bash
# Usar arquivo scale
docker-compose -f docker-compose.scale.yml up -d --scale app=5

# Ver quantas instâncias estão rodando
docker-compose -f docker-compose.scale.yml ps app
```

## Parte 5: Otimizações e Testes (5 min)

### 5.1 Testar compressão Gzip

**Linux/Mac:**
```bash
# Requisição normal
curl -I http://localhost/

# Requisição com Accept-Encoding
curl -I -H "Accept-Encoding: gzip" http://localhost/
```

**Windows (PowerShell):**
```powershell
# Requisição normal
Invoke-WebRequest -Uri http://localhost/ -Method Head

# Requisição com Accept-Encoding
$headers = @{"Accept-Encoding"="gzip"}
Invoke-WebRequest -Uri http://localhost/ -Method Head -Headers $headers
```

**Ver no header:** `Content-Encoding: gzip`

### 5.2 Teste de carga simples

**Linux/Mac (com Apache Bench):**
```bash
# Instalar ab se necessário
# Ubuntu/Debian:
sudo apt-get install apache2-utils

# macOS:
brew install httpd

# Teste: 1000 requisições, 10 concorrentes
ab -n 1000 -c 10 http://localhost/
```

**Windows (PowerShell com teste manual):**
```powershell
# Script simples de teste
$jobs = 1..100 | ForEach-Object {
    Start-Job -ScriptBlock {
        Invoke-WebRequest -Uri http://localhost/health
    }
}

# Aguardar todos terminarem
$jobs | Wait-Job | Receive-Job

# Limpar jobs
$jobs | Remove-Job
```

### 5.3 Verificar distribuição de carga

```bash
# Ver logs de cada instância
docker-compose logs app1 | grep "GET /" | wc -l
docker-compose logs app2 | grep "GET /" | wc -l
docker-compose logs app3 | grep "GET /" | wc -l
```

## Checklist de Validação

- [ ] nginx.conf criado e configurado
- [ ] docker-compose.yml atualizado com 3 instâncias
- [ ] Nginx rodando e saudável
- [ ] 3 instâncias da app rodando
- [ ] Load balancing funcionando (requisições distribuídas)
- [ ] Alta disponibilidade testada (parar 1 instância)
- [ ] Compressão Gzip funcionando
- [ ] Logs do Nginx sendo gerados
- [ ] Aplicação acessível via http://localhost
- [ ] Health checks mostrando instância diferente a cada call

## Arquitetura Final

```
Internet
    |
    v
+-------------------+
|      Nginx        | Port 80
|  Load Balancer    |
+-------------------+
    |
    +-- Round Robin --+
    |                 |
    v                 v
+--------+  +--------+  +--------+
| App1   |  | App2   |  | App3   |
| :5000  |  | :5000  |  | :5000  |
+--------+  +--------+  +--------+
    |           |           |
    +-- Shared Backend ----+
                |
        +-------+-------+
        |               |
    +---v---+      +----v----+
    |  DB   |      | Redis   |
    | :5432 |      |  :6379  |
    +-------+      +---------+
```

## Troubleshooting

### Problema: Nginx não encontra backends

```bash
# Ver logs do Nginx
docker-compose logs nginx

# Testar resolução DNS
docker-compose exec nginx nslookup app1
docker-compose exec nginx ping -c 1 app1
```

### Problema: Load balancing não funciona

```bash
# Verificar configuração do upstream
docker-compose exec nginx cat /etc/nginx/conf.d/default.conf

# Recarregar configuração do Nginx
docker-compose exec nginx nginx -s reload
```

### Problema: Uma instância sempre retorna erro

```bash
# Ver logs da instância problemática
docker-compose logs app1

# Verificar health check
docker-compose exec app1 curl http://localhost:5000/health

# Restart da instância
docker-compose restart app1
```

### Problema: Alta latência

```bash
# Ver tempo de resposta de cada instância
time curl http://localhost/health

# Ver conexões ativas
docker-compose exec nginx netstat -an | grep :80
```

## Próximos Passos

No **Lab 03** você vai:
- Implementar health checks avançados
- Configurar logs estruturados e centralizados
- Criar scripts de deploy automatizado
- Implementar backup e restore do banco
- Preparar para produção real

**Parabéns!** Sua aplicação agora tem alta disponibilidade e pode lidar com muito mais carga!