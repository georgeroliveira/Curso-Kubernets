# Guia de Troubleshooting - Módulo 05

## Problemas Comuns e Soluções

### 1. Containers não sobem

#### Sintoma
```
docker-compose up -d
ERROR: Container taskmanager-app1 failed to start
```

#### Diagnóstico

**Linux/Mac:**
```bash
# Ver logs detalhados
docker-compose logs app1

# Ver eventos do Docker
docker events --since 5m

# Verificar se porta está em uso
lsof -i :5000
netstat -tulpn | grep 5000
```

**Windows (PowerShell):**
```powershell
# Ver logs detalhados
docker-compose logs app1

# Verificar se porta está em uso
Get-NetTCPConnection -LocalPort 5000
```

#### Soluções

**A) Porta em uso:**
```bash
# Parar processo usando a porta
# Linux/Mac:
kill -9 $(lsof -t -i:5000)

# Windows PowerShell:
Stop-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess

# Ou mudar porta no .env
echo "APP_PORT=5001" >> .env
```

**B) Erro de build:**
```bash
# Rebuild sem cache
docker-compose build --no-cache

# Ver detalhes do build
docker-compose build --progress=plain
```

**C) Falta de recursos:**
```bash
# Ver uso de recursos
docker stats

# Limpar recursos não utilizados
docker system prune -a

# Ver espaço em disco
df -h  # Linux/Mac
Get-PSDrive  # Windows PowerShell
```

---

### 2. Banco de dados não conecta

#### Sintoma
```
psycopg2.OperationalError: could not connect to server
```

#### Diagnóstico

```bash
# Verificar se container do banco está rodando
docker-compose ps db

# Ver logs do PostgreSQL
docker-compose logs db

# Testar conexão manualmente
docker-compose exec app1 sh
nc -zv db 5432
exit
```

#### Soluções

**A) Banco não está pronto:**
```yaml
# Ajustar health check no docker-compose.yml
depends_on:
  db:
    condition: service_healthy
```

**B) Credenciais incorretas:**
```bash
# Verificar variáveis de ambiente
docker-compose config | grep POSTGRES

# Verificar .env
cat .env

# Testar conexão manual
docker-compose exec db psql -U taskuser -d taskdb -c "SELECT 1"
```

**C) Rede não está funcionando:**
```bash
# Verificar redes
docker network ls
docker network inspect taskmanager_backend

# Recriar rede
docker-compose down
docker network prune
docker-compose up -d
```

---

### 3. Redis não conecta

#### Sintoma
```
redis.exceptions.ConnectionError: Error connecting to Redis
```

#### Diagnóstico

```bash
# Verificar se Redis está rodando
docker-compose ps redis

# Ver logs
docker-compose logs redis

# Testar conexão
docker-compose exec redis redis-cli ping
```

#### Soluções

**A) Senha incorreta:**
```bash
# Verificar senha no .env
grep REDIS_PASSWORD .env

# Testar com senha
docker-compose exec redis redis-cli -a redis123 ping
```

**B) Redis não está pronto:**
```bash
# Aguardar alguns segundos
sleep 10

# Restart do Redis
docker-compose restart redis
```

**C) Aplicação não está usando Redis corretamente:**
```python
# Verificar URL do Redis no código
# Deve ser: redis://:password@redis:6379/0
```

---

### 4. Nginx retorna 502 Bad Gateway

#### Sintoma
```
curl http://localhost
<html>502 Bad Gateway</html>
```

#### Diagnóstico

```bash
# Ver logs do Nginx
docker-compose logs nginx

# Ver logs das apps
docker-compose logs app1 app2 app3

# Verificar upstream
docker-compose exec nginx cat /etc/nginx/conf.d/default.conf
```

#### Soluções

**A) Apps não estão rodando:**
```bash
# Verificar status
docker-compose ps

# Subir apps
docker-compose up -d app1 app2 app3
```

**B) Apps não estão saudáveis:**
```bash
# Verificar health checks
docker-compose ps

# Ver por que health check está falhando
curl http://localhost:5000/health  # Se exposto
docker-compose exec app1 curl http://localhost:5000/health
```

**C) Configuração do Nginx incorreta:**
```bash
# Verificar sintaxe
docker-compose exec nginx nginx -t

# Recarregar config
docker-compose exec nginx nginx -s reload
```

---

### 5. Dados não persistem após restart

#### Sintoma
```
docker-compose restart
# Todas as tarefas sumiram
```

#### Diagnóstico

```bash
# Verificar volumes
docker volume ls

# Ver detalhes do volume
docker volume inspect taskmanager_postgres_data

# Verificar se volume está montado
docker-compose exec db df -h
```

#### Soluções

**A) Volume não está configurado:**
```yaml
# Verificar docker-compose.yml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

**B) Usando docker-compose down -v por engano:**
```bash
# NUNCA use -v em produção (remove volumes)
docker-compose down     # OK
docker-compose down -v  # Remove dados!
```

**C) Volume corrompido:**
```bash
# Backup dos dados primeiro!
./scripts/backup.sh

# Remover volume corrompido
docker-compose down
docker volume rm taskmanager_postgres_data

# Recriar e restaurar
docker-compose up -d
./scripts/restore.sh
```

---

### 6. Health checks sempre falham

#### Sintoma
```
docker-compose ps
taskmanager-app1    Up (unhealthy)
```

#### Diagnóstico

```bash
# Ver logs do container
docker-compose logs app1

# Testar health check manualmente
docker-compose exec app1 curl -f http://localhost:5000/health

# Ver configuração do health check
docker inspect taskmanager-app1 | grep -A 10 Healthcheck
```

#### Soluções

**A) curl não está instalado na imagem:**
```dockerfile
# Adicionar no Dockerfile
RUN apt-get update && apt-get install -y curl
```

**B) Timeout muito curto:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s      # Aumentar se necessário
  retries: 3
  start_period: 60s  # Aumentar para apps lentas
```

**C) Endpoint /health não existe ou está com erro:**
```bash
# Verificar se rota existe
docker-compose exec app1 curl http://localhost:5000/health

# Ver código da rota no app.py
```

---

### 7. Load balancing não funciona

#### Sintoma
```
# Sempre responde a mesma instância
curl http://localhost/health
{"instance": "app1"}
curl http://localhost/health
{"instance": "app1"}
```

#### Diagnóstico

```bash
# Ver configuração do upstream no Nginx
docker-compose exec nginx cat /etc/nginx/conf.d/default.conf

# Ver logs do Nginx
docker-compose logs nginx

# Verificar se todas as instâncias estão UP
docker-compose ps app1 app2 app3
```

#### Soluções

**A) Apenas uma instância rodando:**
```bash
# Subir todas as instâncias
docker-compose up -d app1 app2 app3
```

**B) Configuração upstream incorreta:**
```nginx
# Verificar se upstream está correto
upstream taskmanager_backend {
    server app1:5000;
    server app2:5000;
    server app3:5000;
}
```

**C) ip_hash ativo (sticky sessions):**
```nginx
# Se usar ip_hash, sempre vai para mesma instância do mesmo IP
upstream taskmanager_backend {
    # ip_hash;  # Comentar esta linha
    server app1:5000;
    server app2:5000;
    server app3:5000;
}
```

---

### 8. Performance lenta

#### Sintoma
```
curl http://localhost
# Demora mais de 5 segundos para responder
```

#### Diagnóstico

```bash
# Ver uso de recursos
docker stats

# Ver logs de todas as apps
docker-compose logs --tail=100

# Testar tempo de resposta
time curl http://localhost/health

# Ver conexões no PostgreSQL
docker-compose exec db psql -U taskuser -d taskdb -c "SELECT count(*) FROM pg_stat_activity"
```

#### Soluções

**A) Falta de recursos:**
```bash
# Ver limites no docker-compose.prod.yml
# Aumentar se necessário

# Verificar memória disponível no host
free -h  # Linux
vm_stat  # Mac
```

**B) Cache não está funcionando:**
```bash
# Verificar se Redis está respondendo
docker-compose exec redis redis-cli ping

# Ver hit rate do cache nos logs
docker-compose logs app1 | grep "cache"
```

**C) Muitas conexões no banco:**
```bash
# Ver conexões ativas
docker-compose exec db psql -U taskuser -d taskdb -c "
  SELECT datname, count(*) 
  FROM pg_stat_activity 
  GROUP BY datname
"

# Configurar connection pool na aplicação
```

**D) Nginx buffer muito pequeno:**
```nginx
# Aumentar buffers no nginx.conf
proxy_buffer_size 8k;
proxy_buffers 16 8k;
proxy_busy_buffers_size 16k;
```

---

### 9. Logs não aparecem

#### Sintoma
```
docker-compose logs
# Nenhum output ou muito pouco
```

#### Diagnóstico

```bash
# Ver se containers estão rodando
docker-compose ps

# Ver logs específicos
docker-compose logs app1

# Verificar se pastas de logs existem
ls -la logs/
```

#### Soluções

**A) Aplicação não está logando:**
```python
# Verificar se logger está configurado no app.py
from logger import logger
logger.info("Aplicação iniciada")
```

**B) Volumes de logs não montados:**
```yaml
# Verificar docker-compose.yml
volumes:
  - ./logs/app1:/app/logs
```

**C) Permissões incorretas:**
```bash
# Linux/Mac
chmod -R 777 logs/

# Verificar owner dos arquivos
ls -la logs/
```

---

### 10. Erro de permissão no PostgreSQL

#### Sintoma
```
psycopg2.errors.InsufficientPrivilege: permission denied for table tasks
```

#### Diagnóstico

```bash
# Conectar no banco
docker-compose exec db psql -U taskuser -d taskdb

# Verificar permissões
\dp tasks

# Ver grants
\du taskuser
```

#### Soluções

**A) Usuário sem permissões:**
```sql
-- Dar todas as permissões para o usuário
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO taskuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO taskuser;
```

**B) Script de inicialização não rodou:**
```bash
# Remover volume e recriar
docker-compose down -v
docker-compose up -d

# O script config/init.sql será executado automaticamente
```

---

### 11. Windows: Problemas com line endings

#### Sintoma
```
/bin/bash^M: bad interpreter
```

#### Solução

```bash
# Converter line endings de CRLF para LF
# Git Bash:
dos2unix scripts/*.sh

# Ou configurar Git para não converter
git config --global core.autocrlf false
```

---

### 12. Windows: Docker não inicia

#### Sintoma
```
docker: Cannot connect to the Docker daemon
```

#### Soluções

**A) Docker Desktop não está rodando:**
```
- Abrir Docker Desktop
- Aguardar inicialização completa
```

**B) WSL2 não está configurado:**
```powershell
# Instalar WSL2
wsl --install
wsl --set-default-version 2

# Restart do computador
```

**C) Virtualização não está habilitada:**
```
- Entrar na BIOS
- Habilitar Intel VT-x ou AMD-V
- Habilitar Hyper-V no Windows
```

---

### 13. Backup falha

#### Sintoma
```
./scripts/backup.sh
ERROR: pg_dump failed
```

#### Diagnóstico

```bash
# Verificar se container do banco está rodando
docker-compose ps db

# Testar pg_dump manualmente
docker-compose exec db pg_dump --version

# Ver logs do banco
docker-compose logs db
```

#### Soluções

**A) Container não está rodando:**
```bash
docker-compose up -d db
```

**B) Permissões no diretório de backup:**
```bash
# Linux/Mac
mkdir -p backups
chmod 755 backups

# Windows
New-Item -Path backups -ItemType Directory -Force
```

**C) Falta de espaço em disco:**
```bash
# Verificar espaço
df -h  # Linux/Mac
Get-PSDrive  # Windows

# Limpar espaço se necessário
docker system prune -a
```

---

### 14. Deploy script falha

#### Sintoma
```
./scripts/deploy.sh
Health check failed after 10 attempts
```

#### Diagnóstico

```bash
# Ver logs de todos os serviços
docker-compose logs

# Ver status
docker-compose ps

# Testar health check manualmente
curl http://localhost/health
```

#### Soluções

**A) Aplicação demora para iniciar:**
```bash
# Aumentar timeout no deploy.sh
# Mudar de:
sleep 30
# Para:
sleep 60
```

**B) Erro no código:**
```bash
# Ver logs da aplicação
docker-compose logs app1 app2 app3

# Verificar sintaxe Python
docker-compose exec app1 python -m py_compile app.py
```

**C) Dependências faltando:**
```bash
# Rebuild completo
docker-compose build --no-cache
```

---

## Comandos de Diagnóstico Rápido

### Health Check Completo

**Linux/Mac:**
```bash
#!/bin/bash
echo "=== Status dos Containers ==="
docker-compose ps

echo ""
echo "=== Health Checks ==="
curl -s http://localhost/health | jq '.'

echo ""
echo "=== Uso de Recursos ==="
docker stats --no-stream

echo ""
echo "=== Volumes ==="
docker volume ls | grep taskmanager

echo ""
echo "=== Redes ==="
docker network ls | grep taskmanager

echo ""
echo "=== Últimos Logs ==="
docker-compose logs --tail=5
```

**Windows (PowerShell):**
```powershell
Write-Host "=== Status dos Containers ==="
docker-compose ps

Write-Host "`n=== Health Checks ==="
Invoke-RestMethod http://localhost/health | ConvertTo-Json

Write-Host "`n=== Uso de Recursos ==="
docker stats --no-stream

Write-Host "`n=== Volumes ==="
docker volume ls | Select-String taskmanager

Write-Host "`n=== Redes ==="
docker network ls | Select-String taskmanager

Write-Host "`n=== Últimos Logs ==="
docker-compose logs --tail=5
```

---

## Quando pedir ajuda

Se nenhuma solução acima funcionou:

1. **Colete informações:**
```bash
# Salvar em arquivo
docker-compose ps > debug.txt
docker-compose logs >> debug.txt
docker version >> debug.txt
docker-compose version >> debug.txt
uname -a >> debug.txt  # Linux/Mac
systeminfo >> debug.txt  # Windows
```

2. **Teste básico:**
```bash
# Teste mínimo
docker run hello-world
```

3. **Reset completo (último recurso):**
```bash
# CUIDADO: Remove TUDO
docker-compose down -v
docker system prune -a --volumes
docker-compose up -d
```

4. **Compartilhe:**
- Arquivo debug.txt
- Versão do Docker e Docker Compose
- Sistema operacional
- Arquivo docker-compose.yml
- Logs de erro específicos

---

## Prevenção de Problemas

### Boas Práticas

1. **Sempre fazer backup antes de mudanças:**
```bash
./scripts/backup.sh
```

2. **Testar em desenvolvimento primeiro:**
```bash
# Usar docker-compose.yml para dev
# Usar docker-compose.prod.yml para produção
```

3. **Monitorar recursos:**
```bash
docker stats
```

4. **Manter logs organizados:**
```bash
# Rotacionar logs grandes
find logs/ -name "*.log" -size +100M -delete
```

5. **Atualizar regularmente:**
```bash
docker-compose pull
docker-compose build --pull
```

6. **Documentar mudanças:**
```bash
# Usar Git para versionamento
git commit -m "Atualização do nginx.conf"
```

---

## Recursos Adicionais

- [Docker Compose Troubleshooting](https://docs.docker.com/compose/faq/)
- [PostgreSQL Common Errors](https://www.postgresql.org/docs/current/errcodes-appendix.html)
- [Nginx Troubleshooting](https://nginx.org/en/docs/debugging_log.html)
- [Redis Troubleshooting](https://redis.io/topics/problems)