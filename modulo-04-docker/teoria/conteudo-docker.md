# Docker para Iniciantes em DevOps

## Como Voce Vai Trabalhar Neste Modulo

Voce vai usar o **VSCode no seu computador local** (Windows/Mac/Linux) conectado via **Remote SSH na VM Ubuntu**.

### O que isso significa?
- Edita arquivos como se estivessem no seu computador
- Arquivos realmente estao na VM (servidor)
- Docker roda **dentro da VM**, nao no seu computador
- Simula ambiente profissional real

### Por que trabalhar assim?
DevOps profissionais trabalham com containers em servidores remotos. Voce esta aprendendo o jeito certo desde o inicio.

---

## Por que aprender Docker?

### Sem Docker - Problemas Comuns

**"Funciona na minha maquina"**
- App funciona no dev, quebra em producao
- Dependencias diferentes entre ambientes
- Versoes conflitantes de bibliotecas
- Configuracoes especificas do SO

**Configuracao manual**
- Instalar Python, bibliotecas, dependencias
- Configurar variaveis de ambiente
- Repetir processo em cada servidor
- Erros humanos em cada instalacao

**Isolamento inexistente**
- Apps competem por recursos
- Conflitos de portas
- Bibliotecas incompativeis
- Um app quebra outro

### Com Docker - Solucoes

- Ambiente identico em dev, staging, producao
- Dependencias empacotadas com aplicacao
- Isolamento completo entre aplicacoes
- Deploy rapido e previsivel
- Rollback instantaneo

---

## Docker vs Maquinas Virtuais

### Maquina Virtual (VM)
```
[App A] [App B]
[Guest OS A] [Guest OS B]
[Hypervisor]
[Host OS]
[Hardware]
```

**Caracteristicas:**
- Sistema operacional completo por app
- Pesado (GB de espaco)
- Lento para iniciar (minutos)
- Isolamento forte
- Usa muita RAM/CPU

### Container Docker
```
[App A] [App B] [App C]
[Docker Engine]
[Host OS]
[Hardware]
```

**Caracteristicas:**
- Compartilha kernel do host
- Leve (MB de espaco)
- Rapido para iniciar (segundos)
- Isolamento suficiente
- Usa menos recursos

### Comparacao Pratica

| Aspecto | VM | Container |
|---------|-----|-----------|
| Tamanho | 1-10 GB | 10-500 MB |
| Startup | 30-60 seg | 1-2 seg |
| Recursos | Alto | Baixo |
| Isolamento | Total | Processo |
| Portabilidade | Media | Alta |

---

## Conceitos Fundamentais

### 1. Imagem Docker

**O que e:** Template somente-leitura com tudo que app precisa.

**Contem:**
- Sistema operacional base (ex: Ubuntu, Alpine)
- Runtime (Python, Node.js, Java)
- Codigo da aplicacao
- Bibliotecas e dependencias
- Arquivos de configuracao

**Analogia:** Imagem e como um ISO de CD - voce nao modifica, apenas usa para criar copias.

**Exemplo:**
```
python:3.11-slim  (imagem oficial Python)
taskmanager:v1    (sua aplicacao)
nginx:alpine      (servidor web)
```

---

### 2. Container

**O que e:** Instancia em execucao de uma imagem.

**Caracteristicas:**
- Executavel e isolado
- Pode ler/escrever durante execucao
- Descartavel (pode ser removido sem perder imagem)
- Leve e rapido

**Analogia:** Se imagem e o programa instalador, container e o programa rodando.

**Ciclo de vida:**
```
Imagem -> Container (rodando) -> Container (parado) -> Removido
```

---

### 3. Dockerfile

**O que e:** Receita para construir uma imagem.

**Estrutura basica:**
```dockerfile
FROM python:3.11-slim      # Imagem base
WORKDIR /app               # Diretorio de trabalho
COPY requirements.txt .    # Copiar arquivos
RUN pip install -r req...  # Executar comandos
COPY . .                   # Copiar codigo
EXPOSE 5000                # Porta exposta
CMD ["python", "app.py"]   # Comando inicial
```

**Instrucoes principais:**

- `FROM` - Imagem base
- `WORKDIR` - Define diretorio de trabalho
- `COPY` - Copia arquivos do host para imagem
- `ADD` - Como COPY, mas com recursos extras (descompactar, URLs)
- `RUN` - Executa comando durante build
- `ENV` - Define variaveis de ambiente
- `EXPOSE` - Documenta porta usada
- `CMD` - Comando padrao ao iniciar container
- `ENTRYPOINT` - Comando fixo ao iniciar
- `VOLUME` - Define ponto de montagem para dados

---

### 4. Registry

**O que e:** Repositorio de imagens Docker.

**Tipos:**
- **Docker Hub** (publico) - hub.docker.com
- **Registry privado** - AWS ECR, Google GCR, Azure ACR
- **Registry local** - Para desenvolvimento

**Operacoes:**
```bash
docker pull python:3.11        # Baixar imagem
docker push user/app:v1        # Enviar imagem
docker search nginx            # Buscar imagens
```

---

### 5. Volume

**O que e:** Armazenamento persistente fora do container.

**Por que usar:**
- Dados sobrevivem ao container
- Compartilhar dados entre containers
- Performance melhor que bind mounts
- Backup e restore facilitados

**Tipos de montagem:**

**Volume nomeado (recomendado):**
```bash
docker volume create mydata
docker run -v mydata:/app/data myapp
```

**Bind mount:**
```bash
docker run -v /host/path:/container/path myapp
```

**tmpfs (memoria):**
```bash
docker run --tmpfs /app/temp myapp
```

---

### 6. Network

**O que e:** Rede virtual para comunicacao entre containers.

**Modos de rede:**

- `bridge` (padrao) - Rede privada, containers se comunicam
- `host` - Usa rede do host diretamente
- `none` - Sem rede
- `overlay` - Para Swarm (cluster)

**Exemplo:**
```bash
docker network create mynet
docker run --network mynet --name app1 myapp
docker run --network mynet --name app2 myapp
# app1 e app2 podem se comunicar por nome
```

---

## Comandos Docker Essenciais

### Gerenciamento de Imagens

```bash
# Listar imagens locais
docker images

# Baixar imagem do Docker Hub
docker pull python:3.11-slim

# Construir imagem do Dockerfile
docker build -t myapp:v1 .

# Construir sem cache
docker build --no-cache -t myapp:v1 .

# Construir com Dockerfile customizado
docker build -f Dockerfile.prod -t myapp:prod .

# Remover imagem
docker rmi myapp:v1

# Remover imagens nao usadas
docker image prune

# Ver historico de layers da imagem
docker history myapp:v1

# Inspecionar imagem (JSON)
docker inspect myapp:v1
```

---

### Gerenciamento de Containers

```bash
# Executar container (foreground)
docker run myapp

# Executar container (background)
docker run -d myapp

# Executar com nome customizado
docker run -d --name mycontainer myapp

# Mapear porta host:container
docker run -d -p 8080:5000 myapp

# Passar variaveis de ambiente
docker run -d -e ENV=production myapp

# Montar volume
docker run -d -v mydata:/app/data myapp

# Listar containers rodando
docker ps

# Listar todos containers (incluindo parados)
docker ps -a

# Ver logs do container
docker logs mycontainer

# Seguir logs em tempo real
docker logs -f mycontainer

# Parar container
docker stop mycontainer

# Iniciar container parado
docker start mycontainer

# Reiniciar container
docker restart mycontainer

# Remover container
docker rm mycontainer

# Remover container rodando (forca)
docker rm -f mycontainer

# Remover todos containers parados
docker container prune
```

---

### Interacao com Containers

```bash
# Executar comando em container rodando
docker exec mycontainer ls /app

# Abrir shell interativo
docker exec -it mycontainer bash

# Copiar arquivo host -> container
docker cp local.txt mycontainer:/app/

# Copiar arquivo container -> host
docker cp mycontainer:/app/log.txt ./

# Ver processos do container
docker top mycontainer

# Ver uso de recursos (CPU, RAM)
docker stats mycontainer

# Inspecionar configuracao (JSON)
docker inspect mycontainer

# Ver portas mapeadas
docker port mycontainer
```

---

### Gerenciamento de Volumes

```bash
# Criar volume
docker volume create mydata

# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect mydata

# Remover volume
docker volume rm mydata

# Remover volumes nao usados
docker volume prune
```

---

### Gerenciamento de Redes

```bash
# Criar rede
docker network create mynet

# Listar redes
docker network ls

# Inspecionar rede
docker network inspect mynet

# Conectar container a rede
docker network connect mynet mycontainer

# Desconectar container da rede
docker network disconnect mynet mycontainer

# Remover rede
docker network rm mynet
```

---

### Limpeza e Manutencao

```bash
# Remover containers parados
docker container prune

# Remover imagens nao usadas
docker image prune

# Remover volumes nao usados
docker volume prune

# Remover redes nao usadas
docker network prune

# Limpeza completa (tudo nao usado)
docker system prune

# Limpeza agressiva (incluindo imagens)
docker system prune -a

# Ver espaco usado
docker system df
```

---

## Dockerfile - Boas Praticas

### 1. Use Imagens Base Especificas

**Ruim:**
```dockerfile
FROM python
```

**Bom:**
```dockerfile
FROM python:3.11-slim
```

**Por que:** Versao especifica evita surpresas, slim e menor.

---

### 2. Minimize Layers

**Ruim:**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
```

**Bom:**
```dockerfile
RUN apt-get update && \
    apt-get install -y curl vim && \
    rm -rf /var/lib/apt/lists/*
```

**Por que:** Menos layers = imagem menor e build mais rapido.

---

### 3. Use .dockerignore

**Criar arquivo `.dockerignore`:**
```
.git
.gitignore
node_modules
venv
*.pyc
__pycache__
.env
*.log
```

**Por que:** Evita copiar arquivos desnecessarios para imagem.

---

### 4. Ordene Comandos por Frequencia de Mudanca

**Ruim:**
```dockerfile
COPY . .
RUN pip install -r requirements.txt
```

**Bom:**
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

**Por que:** Cache de layers funciona melhor, rebuild mais rapido.

---

### 5. Nao Execute como Root

**Ruim:**
```dockerfile
CMD ["python", "app.py"]
```

**Bom:**
```dockerfile
RUN useradd -r appuser
USER appuser
CMD ["python", "app.py"]
```

**Por que:** Seguranca - limita danos se container for comprometido.

---

### 6. Use Multi-stage Builds

**Exemplo:**
```dockerfile
# Stage 1: Build
FROM python:3.11 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . .
CMD ["python", "app.py"]
```

**Por que:** Imagem final nao contem ferramentas de build, fica menor.

---

### 7. Adicione Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

**Por que:** Docker pode detectar e reiniciar containers nao saudaveis.

---

### 8. Use EXPOSE para Documentacao

```dockerfile
EXPOSE 5000
```

**Por que:** Documenta qual porta o app usa (nao abre porta automaticamente).

---

### 9. Defina Variaveis de Ambiente

```dockerfile
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
```

**Por que:** Comportamento consistente e configuravel.

---

## Volumes - Persistencia de Dados

### Por que Usar Volumes?

**Sem volume:**
```bash
docker run myapp
# Criar dados
docker stop myapp
docker rm myapp
# Dados perdidos
```

**Com volume:**
```bash
docker run -v mydata:/app/data myapp
# Criar dados
docker stop myapp
docker rm myapp
docker run -v mydata:/app/data myapp
# Dados preservados
```

---

### Tipos de Volumes

**1. Volume nomeado (recomendado para producao):**
```bash
docker volume create appdata
docker run -v appdata:/app/data myapp
```

**Vantagens:**
- Gerenciado pelo Docker
- Facil backup
- Portavel entre containers

---

**2. Bind mount (bom para desenvolvimento):**
```bash
docker run -v $(pwd)/local:/app/data myapp
```

**Vantagens:**
- Acesso direto aos arquivos
- Sincronizacao em tempo real
- Bom para desenvolvimento

**Desvantagens:**
- Dependente do caminho do host
- Problemas de permissao

---

**3. tmpfs (dados temporarios):**
```bash
docker run --tmpfs /app/temp:rw,size=100m myapp
```

**Uso:** Cache, sessoes temporarias, dados sensiveis.

---

### Backup e Restore

**Backup:**
```bash
docker run --rm -v mydata:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data
```

**Restore:**
```bash
docker run --rm -v mydata:/data -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /
```

---

## Network - Comunicacao entre Containers

### Bridge Network (padrao)

```bash
# Criar rede
docker network create myapp-net

# Executar containers na mesma rede
docker run -d --network myapp-net --name web myapp
docker run -d --network myapp-net --name db postgres

# web pode acessar db por nome:
# psql -h db -U postgres
```

---

### Host Network

```bash
docker run --network host myapp
```

**Uso:** Performance maxima, sem isolamento de rede.

**Desvantagem:** Conflitos de porta com host.

---

### None Network

```bash
docker run --network none myapp
```

**Uso:** Isolamento total de rede, seguranca maxima.

---

## Fluxo de Trabalho DevOps com Docker

### 1. Desenvolvimento Local

```bash
# Criar Dockerfile
vim Dockerfile

# Build da imagem
docker build -t myapp:dev .

# Executar localmente
docker run -d -p 5000:5000 myapp:dev

# Testar
curl http://localhost:5000

# Ver logs
docker logs -f <container>
```

---

### 2. Versionamento

```bash
# Build com tag de versao
docker build -t myapp:1.0.0 .

# Tag como latest
docker tag myapp:1.0.0 myapp:latest

# Versionar Dockerfile
git add Dockerfile
git commit -m "adiciona Dockerfile v1.0.0"
git tag v1.0.0
```

---

### 3. Registry (CI/CD)

```bash
# Login no Docker Hub
docker login

# Tag para registry
docker tag myapp:1.0.0 username/myapp:1.0.0

# Push para registry
docker push username/myapp:1.0.0

# Pull em outro servidor
docker pull username/myapp:1.0.0
docker run -d username/myapp:1.0.0
```

---

### 4. Producao

```bash
# Pull da imagem
docker pull myapp:1.0.0

# Executar com configuracao de producao
docker run -d \
  --name myapp-prod \
  --restart unless-stopped \
  -p 80:5000 \
  -v appdata:/app/data \
  -e FLASK_ENV=production \
  myapp:1.0.0

# Monitorar
docker logs -f myapp-prod
docker stats myapp-prod
```

---

### 5. Atualizacao (Blue-Green Deploy)

```bash
# Baixar nova versao
docker pull myapp:1.1.0

# Executar nova versao em porta diferente
docker run -d --name myapp-v2 -p 8080:5000 myapp:1.1.0

# Testar nova versao
curl http://localhost:8080

# Se OK, trocar portas (via proxy reverso)
# Parar versao antiga
docker stop myapp-prod
docker rm myapp-prod
```

---

## Troubleshooting Comum

### Container nao inicia

```bash
# Ver logs de erro
docker logs <container>

# Ver ultimas linhas
docker logs --tail 50 <container>

# Executar interativamente para debug
docker run -it myapp bash
```

---

### Porta ja em uso

```bash
# Verificar quem usa a porta
sudo lsof -i :5000

# Usar porta diferente
docker run -p 5001:5000 myapp
```

---

### Build muito lento

```bash
# Usar cache do Docker
docker build -t myapp .

# Verificar o que esta sendo copiado
# Adicionar arquivos desnecessarios no .dockerignore

# Build sem cache (ultima opcao)
docker build --no-cache -t myapp .
```

---

### Disco cheio

```bash
# Ver espaco usado
docker system df

# Limpar containers parados
docker container prune

# Limpar imagens nao usadas
docker image prune -a

# Limpar volumes nao usados
docker volume prune

# Limpeza completa
docker system prune -a --volumes
```

---

### Nao consegue acessar container

```bash
# Verificar se container esta rodando
docker ps

# Verificar logs
docker logs <container>

# Testar dentro do container
docker exec -it <container> bash
curl http://localhost:5000

# Verificar porta mapeada
docker port <container>
```

---

## Docker vs Docker Compose

**Docker:** Gerencia containers individuais.
**Docker Compose:** Gerencia multiplos containers como aplicacao.

**Exemplo Docker (manual):**
```bash
docker network create mynet
docker run -d --network mynet --name db postgres
docker run -d --network mynet --name web myapp
```

**Exemplo Docker Compose (automatico):**
```yaml
version: '3'
services:
  db:
    image: postgres
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
```

```bash
docker-compose up -d
```

**Proximo modulo:** Docker Compose para orquestracao.

---

## Resumo

Docker e fundamental para DevOps porque:

- Ambiente consistente em dev/staging/prod
- Deploy rapido e confiavel
- Isolamento de aplicacoes
- Uso eficiente de recursos
- Portabilidade total
- Facilita CI/CD
- Ecosistema maduro e amplo

**Agora e hora de praticar! Va para os labs e containerize o TaskManager.**

---

**Nota:** Este conteudo e material de referencia. Consulte durante e apos os labs sempre que tiver duvidas sobre conceitos ou comandos.