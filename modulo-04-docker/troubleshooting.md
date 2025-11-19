# Troubleshooting - Módulo 04: Docker

Soluções rápidas para os 10 problemas mais comuns.

---

## 1. Docker não está instalado

**Você vê:**
```
docker: command not found
```

**Solução:**
```bash
# Instalar Docker na VM Ubuntu
sudo apt update
sudo apt install docker.io -y

# Iniciar serviço
sudo systemctl start docker
sudo systemctl enable docker

# Verificar instalação
docker --version
```

---

## 2. Permissão negada ao executar docker

**Você vê:**
```
permission denied while trying to connect to the Docker daemon socket
```

**Solução:**
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# IMPORTANTE: Fazer logout e login novamente
exit

# Após login, testar
docker ps
```

---

## 3. Porta já em uso

**Você vê:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:5000: bind: address already in use
```

**Solução:**
```bash
# Verificar processo usando porta
sudo lsof -i :5000

# Parar container usando a porta
docker ps
docker stop <container_id>

# Ou usar porta diferente
docker run -p 5001:5000 taskmanager
```

---

## 4. Build falha - requirements.txt não encontrado

**Você vê:**
```
COPY failed: file not found in build context
```

**Solução:**
```bash
# Verificar se está no diretório correto
pwd
# Deve mostrar: /home/devops/devops-bootcamp/taskmanager-starter

# Verificar se arquivo existe
ls -la requirements.txt

# Se não existe, criar
cat > requirements.txt << 'EOL'
Flask==2.3.3
python-dotenv==1.0.0
gunicorn==21.2.0
Werkzeug==2.3.7
prometheus-client==0.19.0
EOL
```

---

## 5. Container inicia mas não responde

**Você vê:**
- Container rodando: `docker ps` mostra container
- Curl falha: `curl: (7) Failed to connect`

**Solução:**
```bash
# Ver logs do container
docker logs <container_name>

# Verificar erros no app
docker exec -it <container_name> bash
curl http://localhost:5000

# Verificar porta mapeada
docker port <container_name>

# Testar health check
curl http://localhost:5000/health
```

---

## 6. Imagem muito grande (>500MB)

**Você vê:**
```bash
docker images
# taskmanager   latest   abc123   800MB
```

**Solução:**
```bash
# Verificar se está usando python:3.11-slim
grep FROM Dockerfile
# Deve mostrar: FROM python:3.11-slim

# Verificar se .dockerignore existe
ls -la .dockerignore

# Adicionar ao .dockerignore:
echo "venv/" >> .dockerignore
echo "__pycache__/" >> .dockerignore

# Rebuild
docker build -t taskmanager:slim .
```

---

## 7. Volume não persiste dados

**Você vê:**
- Cria tarefas
- Para container
- Inicia novamente
- Tarefas desapareceram

**Solução:**
```bash
# Verificar se volume foi criado
docker volume ls | grep taskmanager

# Criar volume se não existe
docker volume create taskmanager-data

# Executar com volume correto
docker run -d -p 5000:5000 \
  --name taskmanager-app \
  -v taskmanager-data:/app/data \
  taskmanager

# Verificar montagem
docker inspect taskmanager-app | grep -A 10 Mounts
```

---

## 8. Build muito lento (>5 minutos)

**Problema:**
- Build demora muito
- Sempre reinstala tudo

**Solução:**
```bash
# Verificar ordem no Dockerfile
# CORRETO (requirements antes do código):
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .

# ERRADO (código antes):
# COPY . .
# RUN pip install -r requirements.txt

# Usar cache
docker build -t taskmanager .

# Limpar cache se necessário
docker builder prune
```

---

## 9. Erro ao executar health check

**Você vê:**
```bash
docker inspect <container> | grep Health
# "Status": "unhealthy"
```

**Solução:**
```bash
# Verificar se curl está instalado no container
docker exec <container> which curl

# Se não tiver, ajustar Dockerfile:
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends curl

# Testar health check manualmente
docker exec <container> curl -f http://localhost:5000/health

# Verificar logs
docker logs <container>
```

---

## 10. Não consegue entrar no container

**Você vê:**
```
docker exec -it taskmanager bash
OCI runtime exec failed: exec failed: unable to start container process
```

**Solução:**
```bash
# Tentar com sh em vez de bash
docker exec -it taskmanager sh

# Verificar se container está rodando
docker ps

# Ver status do container
docker inspect taskmanager | grep Status

# Se container não tem shell, ver logs
docker logs taskmanager
```

---

## Disco cheio

**Você vê:**
```
no space left on device
```

**Solução:**
```bash
# Ver espaço usado
docker system df

# Limpar containers parados
docker container prune -f

# Limpar imagens não usadas
docker image prune -a -f

# Limpar volumes não usados
docker volume prune -f

# Limpeza completa
docker system prune -a --volumes -f

# Verificar espaço
df -h
```

---

## Comandos úteis para diagnóstico
```bash
# Verificar versão
docker --version
docker info

# Ver logs detalhados
docker logs --tail 100 <container>
docker logs -f <container>

# Inspecionar container
docker inspect <container>

# Ver processos
docker top <container>

# Ver uso de recursos
docker stats <container>

# Verificar rede
docker network ls
docker network inspect bridge

# Verificar volumes
docker volume ls
docker volume inspect <volume>

# Ver histórico da imagem
docker history taskmanager

# Executar comando no container
docker exec <container> <comando>
```

---

## Quando chamar o instrutor

- Problema não está nesta lista
- Seguiu solução mas erro continua
- Docker não instala após múltiplas tentativas
- Container funciona mas aplicação não responde
- Erro de permissão persiste após logout/login

---

Versão: 1.0 - Módulo 04 Docker
Atualizado: 2025
