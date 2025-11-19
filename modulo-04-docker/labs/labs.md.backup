# Labs Praticos - Docker Fundamentos

Execute os labs na VM Ubuntu. Cada lab evolui o TaskManager com Docker.

---

## Lab 1: Primeiro Dockerfile (30 min)

### Objetivo
Criar Dockerfile basico para containerizar o TaskManager.

### Passos

#### 1.1 Verificar Docker na VM

```bash
docker --version
docker info
docker run hello-world
```

**Saida esperada:**
```
Hello from Docker!
```

---

#### 1.2 Navegar para projeto TaskManager

```bash
cd ~/devops-bootcamp/taskmanager-starter
ls -la
```

**Deve mostrar:**
```
app.py
config.py
requirements.txt
templates/
static/
README.md
.gitignore
```

---

#### 1.3 Criar primeiro Dockerfile

**No VSCode, criar arquivo:** `Dockerfile`

**Conteudo:**

```dockerfile
# Imagem base Python
FROM python:3.11-slim

# Diretorio de trabalho no container
WORKDIR /app

# Copiar arquivo de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo da aplicacao
COPY . .

# Expor porta da aplicacao
EXPOSE 5000

# Comando para executar a aplicacao
CMD ["python", "app.py"]
```

**Salvar o arquivo** (`Ctrl + S`)

---

#### 1.4 Construir primeira imagem

```bash
docker build -t taskmanager:v1 .
```

**Saida esperada:**
```
[+] Building 45.2s
 => [1/5] FROM docker.io/library/python:3.11-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
 => exporting to image
Successfully tagged taskmanager:v1
```

---

#### 1.5 Verificar imagem criada

```bash
docker images | grep taskmanager
```

**Saida:**
```
taskmanager   v1   abc123   2 minutes ago   180MB
```

---

#### 1.6 Executar container

```bash
docker run -p 5000:5000 taskmanager:v1
```

**Saida esperada:**
```
TaskManager v0.1.0 iniciando...
Ambiente: development
Servidor: http://0.0.0.0:5000
```

---

#### 1.7 Testar aplicacao

**Em outro terminal (ou nova aba):**

```bash
# Via curl
curl http://localhost:5000

# Via navegador na VM
# Abrir: http://localhost:5000
```

**Deve exibir:** Interface do TaskManager funcionando.

---

#### 1.8 Parar container

**No terminal onde container esta rodando:**
```
Ctrl + C
```

**Ou em outro terminal:**
```bash
docker ps
docker stop <container_id>
```

---

#### 1.9 Commitar Dockerfile

```bash
git add Dockerfile
git commit -m "adiciona Dockerfile basico"
```

---

### Checkpoint

Ao final deste lab voce deve ter:

- TaskManager funcionando em container
- Dockerfile criado e versionado
- Compreensao do processo build/run
- Imagem Docker funcional

---

## Lab 2: Comandos Docker Essenciais (45 min)

### Objetivo
Dominar comandos Docker para desenvolvimento e debug.

### Passos

#### 2.1 Listar imagens e containers

```bash
# Ver imagens
docker images

# Ver containers rodando
docker ps

# Ver todos containers (parados tambem)
docker ps -a
```

---

#### 2.2 Executar container em background

```bash
docker run -d -p 5000:5000 --name taskmanager-app taskmanager:v1
```

**Parametros:**
- `-d` - Detached (background)
- `-p 5000:5000` - Mapear porta
- `--name` - Nome do container

**Saida:**
```
abc123def456... (container ID)
```

---

#### 2.3 Verificar container rodando

```bash
docker ps
```

**Saida:**
```
CONTAINER ID   IMAGE            STATUS         PORTS                    NAMES
abc123def456   taskmanager:v1   Up 10 seconds  0.0.0.0:5000->5000/tcp   taskmanager-app
```

---

#### 2.4 Ver logs do container

```bash
# Ver logs
docker logs taskmanager-app

# Seguir logs em tempo real
docker logs -f taskmanager-app
```

**Para parar seguir logs:** `Ctrl + C`

---

#### 2.5 Entrar no container

```bash
docker exec -it taskmanager-app bash
```

**Agora voce esta dentro do container. Explorar:**

```bash
# Listar arquivos
ls -la

# Ver processos
ps aux

# Ver conteudo do app.py
cat app.py

# Sair do container
exit
```

---

#### 2.6 Inspecionar container

```bash
# Informacoes detalhadas (JSON)
docker inspect taskmanager-app

# Verificar porta mapeada
docker port taskmanager-app

# Estatisticas de uso (CPU, RAM)
docker stats taskmanager-app
```

**Para parar stats:** `Ctrl + C`

---

#### 2.7 Parar e remover container

```bash
# Parar container
docker stop taskmanager-app

# Verificar status
docker ps -a

# Remover container
docker rm taskmanager-app

# Verificar remocao
docker ps -a
```

---

#### 2.8 Rebuild com alteracao

**Editar `app.py` no VSCode:**

Localizar a rota `/` e alterar:

```python
@app.route('/')
def index():
    requests_total.labels(method='GET', endpoint='/').inc()
    logger.info("Pagina inicial acessada")
    return """
    <h1>TaskManager - Versao Docker</h1>
    <p><strong>Ambiente:</strong> {}</p>
    <p><strong>Status:</strong> Operacional</p>
    <p><a href='/health'>Health Check</a> | <a href='/metrics'>Metrics</a></p>
    """.format(config.ENVIRONMENT)
```

**Salvar arquivo.**

---

#### 2.9 Rebuild da imagem

```bash
docker build -t taskmanager:v2 .
```

---

#### 2.10 Executar nova versao

```bash
docker run -d -p 5000:5000 --name taskmanager-v2 taskmanager:v2
```

**Testar:**
```bash
curl http://localhost:5000
```

Deve mostrar: **"TaskManager - Versao Docker"**

---

#### 2.11 Limpar containers parados

```bash
# Parar container
docker stop taskmanager-v2

# Limpar todos containers parados
docker container prune -f
```

---

#### 2.12 Commit da alteracao

```bash
git add app.py
git commit -m "atualiza titulo para versao Docker"
```

---

### Checkpoint

Ao final deste lab voce deve ter:

- Comandos Docker dominados
- Debug de containers funcional
- Processo de rebuild compreendido
- Capacidade de inspecionar containers

---

## Lab 3: Volumes e Persistencia (45 min)

### Objetivo
Configurar volumes para persistir dados do TaskManager.

### Passos

#### 3.1 Demonstrar problema: dados perdidos

```bash
# Rodar container
docker run -d -p 5000:5000 --name test-persist taskmanager:v2
```

**Acesse http://localhost:5000 e crie algumas tarefas.**

```bash
# Parar e remover container
docker stop test-persist
docker rm test-persist

# Rodar novamente
docker run -d -p 5000:5000 --name test-persist2 taskmanager:v2
```

**Acesse novamente - tarefas foram perdidas.**

```bash
# Limpar
docker stop test-persist2
docker rm test-persist2
```

---

#### 3.2 Criar volume nomeado

```bash
docker volume create taskmanager-data
```

---

#### 3.3 Listar volumes

```bash
docker volume ls
```

**Saida:**
```
DRIVER    VOLUME NAME
local     taskmanager-data
```

---

#### 3.4 Inspecionar volume

```bash
docker volume inspect taskmanager-data
```

**Mostra:** Localizacao no host, driver, etc.

---

#### 3.5 Executar container com volume

```bash
docker run -d -p 5000:5000 \
  --name taskmanager-persistent \
  -v taskmanager-data:/app/data \
  taskmanager:v2
```

**Parametro:**
- `-v taskmanager-data:/app/data` - Monta volume no path `/app/data` dentro do container

---

#### 3.6 Criar tarefas

**Acesse http://localhost:5000 e crie algumas tarefas.**

---

#### 3.7 Testar persistencia

```bash
# Parar container
docker stop taskmanager-persistent

# Remover container
docker rm taskmanager-persistent

# Rodar novamente com mesmo volume
docker run -d -p 5000:5000 \
  --name taskmanager-persistent2 \
  -v taskmanager-data:/app/data \
  taskmanager:v2
```

**Acesse novamente - tarefas devem estar preservadas.**

---

#### 3.8 Verificar dados no volume

```bash
# Inspecionar volume
docker volume inspect taskmanager-data

# Ver conteudo (requer sudo)
sudo ls -la /var/lib/docker/volumes/taskmanager-data/_data/
```

**Deve mostrar:** `tasks.json` ou arquivos de dados.

---

#### 3.9 Limpar

```bash
docker stop taskmanager-persistent2
docker rm taskmanager-persistent2
```

---

#### 3.10 Commit (se houver alteracoes)

```bash
git status
# Se houver mudancas, commitar
```

---

### Checkpoint

Ao final deste lab voce deve ter:

- Dados persistem entre reinicializacoes
- Volumes Docker configurados
- Compreensao de persistencia em containers

---

## Lab 4: Dockerfile Otimizado (45 min)

### Objetivo
Melhorar Dockerfile com boas praticas de seguranca e eficiencia.

### Passos

#### 4.1 Criar .dockerignore

**No VSCode, criar arquivo:** `.dockerignore`

**Conteudo:**

```
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
*.pyo
.pytest_cache

# Environment
.env
venv/
env/

# IDE
.vscode/
.idea/

# Documentation
README.md
*.md

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Labs
labs.md
```

**Salvar arquivo.**

---

#### 4.2 Criar Dockerfile otimizado

**Substituir conteudo de `Dockerfile`:**

```dockerfile
# Usar imagem especifica e menor
FROM python:3.11-slim

# Metadados
LABEL maintainer="DevOps Bootcamp"
LABEL version="1.0"
LABEL description="TaskManager containerizado"

# Variaveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production

# Criar usuario nao-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar dependencias do sistema (se necessario)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Diretorio de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache de layers)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar codigo da aplicacao
COPY --chown=appuser:appuser . .

# Criar diretorio para dados
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Trocar para usuario nao-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expor porta
EXPOSE 5000

# Comando para executar
CMD ["python", "app.py"]
```

**Salvar arquivo.**

---

#### 4.3 Build da versao otimizada

```bash
docker build -t taskmanager:optimized .
```

---

#### 4.4 Comparar tamanhos das imagens

```bash
docker images | grep taskmanager
```

**Saida exemplo:**
```
taskmanager   optimized   def789   1 minute ago    185MB
taskmanager   v2          abc456   10 minutes ago  190MB
taskmanager   v1          xyz123   30 minutes ago  195MB
```

---

#### 4.5 Testar versao otimizada

```bash
docker run -d -p 5000:5000 \
  --name taskmanager-opt \
  -v taskmanager-data:/app/data \
  taskmanager:optimized
```

---

#### 4.6 Testar health check

```bash
# Aguardar 40 segundos (start-period)
sleep 45

# Verificar health status
docker inspect taskmanager-opt | grep -A 5 Health
```

**Deve mostrar:** `"Status": "healthy"`

---

#### 4.7 Verificar usuario nao-root

```bash
docker exec taskmanager-opt whoami
```

**Saida esperada:**
```
appuser
```

Nao deve ser `root`.

---

#### 4.8 Limpar

```bash
docker stop taskmanager-opt
docker rm taskmanager-opt
```

---

#### 4.9 Commit do Dockerfile otimizado

```bash
git add Dockerfile .dockerignore
git commit -m "otimiza Dockerfile com boas praticas de seguranca"
```

---

### Checkpoint

Ao final deste lab voce deve ter:

- Dockerfile seguindo boas praticas
- Usuario nao-root configurado
- Health check funcionando
- Cache de layers otimizado
- .dockerignore configurado

---

## Lab 5: Multi-stage Build (30 min)

### Objetivo
Criar build multi-estagio para imagem ainda menor.

### Passos

#### 5.1 Criar Dockerfile multi-stage

**Criar novo arquivo:** `Dockerfile.multistage`

**Conteudo:**

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias de build (se necessario)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Criar virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

# Metadados
LABEL maintainer="DevOps Bootcamp"
LABEL version="2.0"
LABEL description="TaskManager multi-stage build"

# Variaveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/opt/venv/bin:$PATH"

# Instalar apenas runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Criar usuario
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copiar virtual environment do builder
COPY --from=builder /opt/venv /opt/venv

# Diretorio de trabalho
WORKDIR /app

# Copiar aplicacao
COPY --chown=appuser:appuser . .

# Criar diretorio de dados
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Trocar usuario
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expor porta
EXPOSE 5000

# Comando
CMD ["python", "app.py"]
```

**Salvar arquivo.**

---

#### 5.2 Build multi-stage

```bash
docker build -f Dockerfile.multistage -t taskmanager:multistage .
```

---

#### 5.3 Comparar tamanhos

```bash
docker images | grep taskmanager
```

**Comparar:** `multistage` deve ser ligeiramente menor que `optimized`.

---

#### 5.4 Testar versao multi-stage

```bash
docker run -d -p 5001:5000 \
  --name taskmanager-multi \
  -v taskmanager-data:/app/data \
  taskmanager:multistage
```

**Nota:** Usando porta 5001 para nao conflitar.

---

#### 5.5 Testar

```bash
curl http://localhost:5001/health
```

**Deve retornar JSON com status healthy.**

---

#### 5.6 Limpar

```bash
docker stop taskmanager-multi
docker rm taskmanager-multi
```

---

#### 5.7 Commit

```bash
git add Dockerfile.multistage
git commit -m "adiciona build multi-stage"
```

---

### Checkpoint

Ao final deste lab voce deve ter:

- Build multi-stage funcionando
- Imagem otimizada para producao
- Comparacao de tamanhos realizada
- Compreensao de multi-stage builds

---

## Lab 6: Preparacao para Docker Compose (30 min)

### Objetivo
Organizar projeto para proximo modulo (Docker Compose).

### Passos

#### 6.1 Verificar estrutura final do projeto

```bash
tree ~/devops-bootcamp/taskmanager-starter
```

**Deve mostrar:**
```
taskmanager-starter/
├── app.py
├── config.py
├── requirements.txt
├── VERSION
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── Dockerfile.multistage
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── README.md
```

---

#### 6.2 Atualizar README.md do projeto

**Adicionar secao Docker ao README.md:**

```markdown

## Docker

### Executar com Docker

#### Build da imagem
```bash
docker build -t taskmanager .
```

#### Executar container
```bash
docker run -d -p 5000:5000 \
  --name taskmanager-app \
  -v taskmanager-data:/app/data \
  taskmanager
```

#### Ver logs
```bash
docker logs taskmanager-app
```

#### Parar container
```bash
docker stop taskmanager-app
docker rm taskmanager-app
```

### Versoes Disponiveis

- `taskmanager:v1` - Versao basica
- `taskmanager:optimized` - Dockerfile otimizado
- `taskmanager:multistage` - Build multi-stage

### Proximo Modulo

Modulo 5 adicionara:
- PostgreSQL database
- Redis cache
- Nginx proxy
- Docker Compose orquestracao
```

**Salvar README.md**

---

#### 6.3 Criar script para desenvolvimento

**Criar arquivo:** `docker-dev.sh`

**Conteudo:**

```bash
#!/bin/bash

echo "TaskManager - Docker Development"
echo "================================"

# Build da imagem
echo "Building image..."
docker build -t taskmanager:dev .

# Para container existente se houver
docker stop taskmanager-dev 2>/dev/null || true
docker rm taskmanager-dev 2>/dev/null || true

# Criar volume se nao existir
docker volume create taskmanager-data 2>/dev/null || true

# Executar container
echo "Starting container..."
docker run -d \
  --name taskmanager-dev \
  -p 5000:5000 \
  -v taskmanager-data:/app/data \
  taskmanager:dev

echo ""
echo "TaskManager disponivel em: http://localhost:5000"
echo "Health check: http://localhost:5000/health"
echo "Logs: docker logs -f taskmanager-dev"
echo ""
```

**Salvar arquivo.**

---

#### 6.4 Tornar script executavel

```bash
chmod +x docker-dev.sh
```

---

#### 6.5 Testar script

```bash
./docker-dev.sh
```

**Deve:** Buildar, iniciar container, e exibir URLs.

---

#### 6.6 Limpeza de imagens antigas

```bash
# Parar todos containers
docker stop $(docker ps -aq) 2>/dev/null || true

# Remover containers parados
docker container prune -f

# Remover imagens nao usadas
docker image prune -f

# Verificar imagens restantes
docker images | grep taskmanager
```

---

#### 6.7 Commit final do modulo

```bash
git add .
git commit -m "finaliza modulo Docker - projeto preparado para Compose"
```

---

#### 6.8 Tag da versao

```bash
git tag -a v1.0-docker -m "TaskManager containerizado - Modulo 4 completo"
```

---

#### 6.9 Ver historico

```bash
git log --oneline --graph --all
```

---

### Checkpoint

Ao final deste lab voce deve ter:

- Projeto organizado e documentado
- Scripts de desenvolvimento prontos
- Versao taggeada no Git
- Preparado para Docker Compose

---

## Projeto Concluido

Parabens! Voce completou o Modulo 4 com:

### Docker Dominado
- Dockerfile criado e otimizado
- Comandos Docker essenciais
- Volumes para persistencia
- Multi-stage builds
- Boas praticas de seguranca

### TaskManager Evoluido
- Aplicacao containerizada
- Dados persistentes
- Health checks funcionando
- Pronto para orquestracao

### Preparado para Modulo 5
- Estrutura organizada
- Documentacao atualizada
- Scripts de desenvolvimento
- Base solida para Docker Compose

O TaskManager agora roda em qualquer ambiente que tenha Docker. No proximo modulo, adicionaremos PostgreSQL e Redis com Docker Compose.