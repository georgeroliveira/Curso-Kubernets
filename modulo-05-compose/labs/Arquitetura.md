# Arquitetura da Stack TaskManager

## Visão Geral

A stack TaskManager é uma aplicação web multi-container orquestrada com Docker Compose, seguindo boas práticas de arquitetura de microserviços e separação de responsabilidades.

## Diagrama de Arquitetura

```
                    [Internet / Cliente]
                            |
                            | HTTP :80
                            v
                    +---------------+
                    |     Nginx     |
                    | Load Balancer |
                    | Proxy Reverso |
                    +---------------+
                            |
            +---------------+---------------+
            |               |               |
            v               v               v
    +-------------+  +-------------+  +-------------+
    | TaskManager |  | TaskManager |  | TaskManager |
    |  Instance 1 |  |  Instance 2 |  |  Instance 3 |
    |  Flask :5000|  |  Flask :5000|  |  Flask :5000|
    +-------------+  +-------------+  +-------------+
            |               |               |
            |               |               |
    [Frontend Network]      |        [Frontend Network]
    ========================|========================
    [Backend Network]       |        [Backend Network]
            |               |               |
            +---------------+---------------+
                            |
            +---------------+---------------+
            |                               |
            v                               v
    +--------------+               +---------------+
    |  PostgreSQL  |               |     Redis     |
    |  Database    |               |     Cache     |
    |    :5432     |               |     :6379     |
    +--------------+               +---------------+
            |                               |
            v                               v
    [postgres_data]                 [redis_data]
     Volume Persistente              Volume Persistente
```

## Componentes da Stack

### 1. Nginx (Proxy Reverso e Load Balancer)

**Função:** Ponto de entrada único para toda a aplicação

**Responsabilidades:**
- Receber todas as requisições HTTP na porta 80
- Distribuir carga entre as 3 instâncias da aplicação (round-robin)
- Compressão Gzip para otimizar transferência
- Cache de arquivos estáticos
- Proxy de headers (X-Real-IP, X-Forwarded-For)
- Health checks dos backends

**Tecnologia:** Nginx Alpine (imagem oficial)

**Portas:**
- 80:80 (HTTP)
- 443:443 (HTTPS - preparado para futuro)

**Configuração:**
```nginx
upstream taskmanager_backend {
    server app1:5000 max_fails=3 fail_timeout=30s;
    server app2:5000 max_fails=3 fail_timeout=30s;
    server app3:5000 max_fails=3 fail_timeout=30s;
}
```

**Alta Disponibilidade:** Se uma instância falhar, Nginx automaticamente remove do pool

---

### 2. TaskManager Application (3 Instâncias)

**Função:** Aplicação web Python Flask

**Responsabilidades:**
- Servir interface web (HTML/CSS/JS)
- API REST para operações CRUD
- Lógica de negócio
- Integração com PostgreSQL (dados)
- Integração com Redis (cache e sessões)
- Health checks (/health, /ready, /live)
- Logs estruturados em JSON

**Tecnologia:** Python 3.11 + Flask 2.3

**Dependências:**
- psycopg2-binary (PostgreSQL)
- redis (Redis)
- python-dotenv (variáveis de ambiente)

**Endpoints:**
- GET `/` - Página principal
- POST `/add` - Criar tarefa
- GET `/complete/<id>` - Marcar como completa
- GET `/delete/<id>` - Deletar tarefa
- GET `/health` - Health check detalhado
- GET `/ready` - Readiness probe
- GET `/live` - Liveness probe

**Instâncias:**
- **app1:** taskmanager-app1
- **app2:** taskmanager-app2
- **app3:** taskmanager-app3

**Por que 3 instâncias?**
- Alta disponibilidade (2 podem falhar e sistema continua)
- Distribuição de carga
- Zero downtime deployments
- Melhor uso de recursos

---

### 3. PostgreSQL Database

**Função:** Banco de dados relacional para persistência

**Responsabilidades:**
- Armazenar usuários
- Armazenar tarefas
- Garantir integridade referencial
- Transações ACID
- Backups e recuperação

**Tecnologia:** PostgreSQL 15 Alpine

**Schema:**
```sql
users
├── id (SERIAL PRIMARY KEY)
├── username (VARCHAR UNIQUE)
├── email (VARCHAR UNIQUE)
├── password_hash (VARCHAR)
└── created_at (TIMESTAMP)

tasks
├── id (SERIAL PRIMARY KEY)
├── user_id (INTEGER → users.id)
├── title (VARCHAR)
├── description (TEXT)
├── completed (BOOLEAN)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

**Índices para Performance:**
- idx_tasks_user_id ON tasks(user_id)
- idx_tasks_completed ON tasks(completed)
- idx_tasks_created_at ON tasks(created_at DESC)

**Volume:** postgres_data (persistente)

**Porta:** 5432 (exposta apenas em dev)

---

### 4. Redis Cache

**Função:** Cache in-memory e gerenciamento de sessões

**Responsabilidades:**
- Cache de consultas frequentes (tarefas por usuário)
- Sessões de usuário (login/logout)
- Rate limiting (futuro)
- Filas de jobs (futuro)

**Tecnologia:** Redis 7 Alpine

**Estrutura de Dados:**
```
tasks:user:<user_id>  → JSON com lista de tarefas
session:<session_id>  → Dados da sessão do usuário
```

**Configuração:**
- Append-only file (AOF) habilitado
- Persistência a cada segundo
- Password-protected

**Volume:** redis_data (persistente)

**Porta:** 6379 (apenas na rede backend)

**TTL:** 5 minutos para cache de tarefas

---

## Redes Docker

### Frontend Network

**Objetivo:** Comunicação entre Nginx e aplicações

**Isolamento:** Acesso externo permitido (porta 80)

**Serviços:**
- nginx
- app1, app2, app3

**Fluxo de Dados:**
```
Internet → Nginx (frontend) → App1/2/3 (frontend)
```

### Backend Network

**Objetivo:** Comunicação entre aplicações e serviços de dados

**Isolamento:** Sem acesso externo direto (internal network)

**Serviços:**
- app1, app2, app3
- db (PostgreSQL)
- redis

**Fluxo de Dados:**
```
App1/2/3 (backend) → PostgreSQL (backend)
App1/2/3 (backend) → Redis (backend)
```

**Benefícios da Separação:**
- Segurança: DB e Redis não expostos diretamente
- Isolamento: Problemas na frontend não afetam backend
- Performance: Tráfego otimizado por rede

---

## Volumes Persistentes

### postgres_data

**Tipo:** Named volume

**Mountpoint:** /var/lib/postgresql/data

**Tamanho:** Dinâmico (cresce conforme necessário)

**Backup:** ./scripts/backup.sh

**Dados Armazenados:**
- Tabelas do PostgreSQL
- Índices
- WAL (Write-Ahead Log)
- Configurações

### redis_data

**Tipo:** Named volume

**Mountpoint:** /data

**Persistência:** AOF (Append-Only File)

**Dados Armazenados:**
- Cache de consultas
- Sessões de usuário
- Dados temporários

### Bind Mounts

**logs/app1, logs/app2, logs/app3:**
- Logs JSON estruturados
- Logs em texto plano
- Facilita debugging

**nginx/nginx.conf:**
- Configuração do Nginx
- Read-only (segurança)

**config/init.sql:**
- Script de inicialização do banco
- Executado apenas na primeira vez

---

## Fluxo de Requisição

### 1. Requisição HTTP Chega

```
Cliente → http://localhost/ → Nginx :80
```

### 2. Nginx Distribui Carga

```
Nginx → [Round Robin] → app1 ou app2 ou app3 :5000
```

### 3. Aplicação Processa

```
App → Verifica cache no Redis
```

**Se CACHE HIT:**
```
Redis → App → Nginx → Cliente
(~10ms de latência)
```

**Se CACHE MISS:**
```
App → Consulta PostgreSQL
PostgreSQL → App
App → Salva no Redis (TTL 5min)
App → Nginx → Cliente
(~50ms de latência)
```

### 4. Operação de Escrita (POST/DELETE)

```
Cliente → Nginx → App → PostgreSQL (INSERT/UPDATE/DELETE)
App → Invalida cache no Redis (DELETE key)
App → Nginx → Cliente
```

---

## Health Checks e Auto-Recovery

### Liveness Probe

**Objetivo:** Verificar se container está vivo (não travado)

**Endpoint:** GET /live

**Ação se falhar:** Restart do container

**Configuração:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/live"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Readiness Probe

**Objetivo:** Verificar se pode receber tráfego

**Endpoint:** GET /ready

**Verifica:**
- Conexão com PostgreSQL OK
- Conexão com Redis OK
- Aplicação inicializada

**Ação se falhar:** Nginx remove do pool (não envia mais requisições)

### Health Check Detalhado

**Endpoint:** GET /health

**Retorna:**
```json
{
  "status": "healthy",
  "instance": {
    "id": "app1",
    "name": "TaskManager-Instance-1"
  },
  "checks": {
    "database": {
      "status": "healthy",
      "response_time_ms": 15.2
    },
    "redis": {
      "status": "healthy",
      "response_time_ms": 2.3
    }
  }
}
```

---

## Estratégia de Logs

### Aplicação (app1/2/3)

**Formato:** JSON estruturado

**Níveis:**
- INFO: Operações normais
- WARNING: Alertas (cache miss, slow query)
- ERROR: Erros de aplicação
- DEBUG: Informações de desenvolvimento

**Exemplo:**
```json
{
  "timestamp": "2025-10-13T10:30:00",
  "level": "INFO",
  "instance": "app1",
  "message": "Task created successfully",
  "task_id": 123,
  "user_id": 1
}
```

**Destino:**
- Console (stdout/stderr)
- Arquivo: /app/logs/app.json.log

### Nginx

**Formato:** Combined Log Format

**Logs:**
- access.log: Todas as requisições
- error.log: Erros e warnings

**Destino:** /var/log/nginx/

### PostgreSQL

**Logs:**
- Queries lentas (> 1s)
- Erros de conexão
- Deadlocks

**Destino:** Container logs (docker logs)

---

## Escalabilidade

### Horizontal Scaling

**Atual:** 3 instâncias da aplicação

**Como escalar:**
```bash
# Adicionar mais instâncias
docker-compose up -d --scale app=5
```

**Limites:**
- CPU/Memória do host
- Conexões do PostgreSQL (max_connections)
- Recursos do Redis

### Vertical Scaling

**Aumentar recursos por container:**
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 1G
```

### Database Scaling

**Leitura:**
- Read replicas do PostgreSQL (futuro)
- PgBouncer para connection pooling

**Escrita:**
- Particionamento de tabelas
- Sharding (muito além do escopo)

---

## Segurança

### Princípios Implementados

**1. Least Privilege:**
- Cada container roda com usuário não-root (quando possível)
- Redes isoladas (backend sem acesso externo)

**2. Secrets Management:**
- Senhas em variáveis de ambiente (.env)
- .env no .gitignore (não commitado)

**3. Network Segmentation:**
- Frontend network: Nginx + Apps
- Backend network: Apps + DB + Redis
- DB e Redis não expostos diretamente

**4. Resource Limits:**
- CPU e memória limitados (docker-compose.prod.yml)
- Previne DoS por exaustão de recursos

**5. Health Checks:**
- Restart automático de containers com problemas
- Nginx remove backends não-saudáveis

### O que falta (para produção real):

- [ ] HTTPS/TLS com Let's Encrypt
- [ ] Firewall (iptables/ufw)
- [ ] Secrets com Docker Secrets ou Vault
- [ ] WAF (Web Application Firewall)
- [ ] Rate limiting no Nginx
- [ ] Scanning de vulnerabilidades (Trivy)
- [ ] Auditoria de acessos

---

## Performance

### Otimizações Implementadas

**1. Cache Redis:**
- Reduz latência de 50ms para 10ms
- TTL de 5 minutos

**2. Índices no PostgreSQL:**
- Consultas rápidas (< 10ms)
- Evita full table scans

**3. Nginx Gzip:**
- Compressão de texto (HTML/CSS/JS)
- Reduz bandwidth em ~70%

**4. Load Balancing:**
- Distribui carga entre 3 instâncias
- Suporta ~300 req/s (depende do hardware)

**5. Connection Pooling:**
- Reutilização de conexões com PostgreSQL
- Reduz overhead de novas conexões

### Métricas Esperadas

**Latência:**
- Cache hit: ~10ms
- Cache miss: ~50ms
- Escrita: ~100ms

**Throughput:**
- 3 instâncias: ~300 req/s
- 5 instâncias: ~500 req/s

**Recursos (por instância):**
- CPU: 5-10% idle, 50-70% sob carga
- RAM: ~200MB por instância

---

## Disaster Recovery

### Backup Strategy

**Frequência:** Diário (cron job)

**Retenção:** 7 dias

**Automação:**
```bash
# Crontab
0 2 * * * cd /opt/taskmanager && ./scripts/backup.sh
```

**Backup inclui:**
- Dump completo do PostgreSQL
- Compressão gzip
- Timestamp no nome do arquivo

### Recovery Process

**RTO (Recovery Time Objective):** < 15 minutos

**RPO (Recovery Point Objective):** < 24 horas

**Passos:**
1. Parar aplicação
2. Restaurar banco do backup
3. Reiniciar aplicação
4. Validar dados

```bash
./scripts/restore.sh
```

---

## Monitoramento (Preparado para Módulo 08)

### Métricas a Coletar

**Aplicação:**
- Requests por segundo
- Latência (p50, p95, p99)
- Taxa de erro (5xx)
- Cache hit rate

**PostgreSQL:**
- Conexões ativas
- Queries lentas
- Tamanho do banco
- Replication lag (se houver)

**Redis:**
- Memory usage
- Hit rate
- Commands per second
- Evictions

**Nginx:**
- Requests por segundo
- Upstream response time
- Error rate
- Active connections

**Sistema:**
- CPU usage
- Memory usage
- Disk usage
- Network I/O

### Alertas Sugeridos

- CPU > 80% por 5 minutos
- Memory > 90%
- Disk > 85%
- Error rate > 5%
- Latência p95 > 500ms
- Health check failing

---

## Comparação: Antes vs Depois

### Módulo 04 (Container Único)

```
[TaskManager Container] :5000
    └── Dados em arquivo JSON
```

**Limitações:**
- Sem escalabilidade
- Sem redundância
- Performance limitada
- Dados não relacionais

### Módulo 05 (Stack Multi-Container)

```
[Nginx] → [App1, App2, App3] → [PostgreSQL + Redis]
```

**Benefícios:**
- Alta disponibilidade
- Escalabilidade horizontal
- Cache para performance
- Dados relacionais
- Load balancing
- Zero downtime deploys

---

## Conclusão

Esta arquitetura implementa:

- **Disponibilidade:** 99.9% uptime (3 instâncias)
- **Performance:** Cache Redis + índices PostgreSQL
- **Escalabilidade:** Horizontal (adicionar instâncias)
- **Segurança:** Redes isoladas, health checks
- **Manutenibilidade:** Logs estruturados, backup automatizado
- **Resiliência:** Auto-recovery, restart policies

É uma arquitetura **production-ready** para aplicações de pequeno a médio porte.