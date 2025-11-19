# Módulo 05 — Docker Compose e Orquestração Completa

O objetivo deste módulo é transformar o TaskManager em uma **arquitetura real**, usando **Docker Compose** para orquestrar múltiplos serviços:

- Flask (aplicação)
- PostgreSQL (banco)
- Redis (cache)
- NGINX (reverse proxy em produção)
- Gunicorn (WSGI)
- Health Checks
- Réplicas
- Volumes persistentes
- Scripts de automação

Este módulo marca a transição do projeto para um ambiente **profissional de DevOps**.

---

# 🚀 1. Arquitetura Final

A estrutura final do módulo:

```

modulo-05-compose/
├── 00-INDICE.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── nginx.conf
├── db/
│   └── init.sql
├── logs/
├── scripts/
│   ├── backup.sh
│   ├── deploy.sh
│   └── restore.sh
└── projeto-taskmanager/
├── app.py
├── config.py
├── Dockerfile
├── VERSION
├── requirements.txt
├── templates/
│   └── index.html
└── static/
└── style.css

````

---

# 🐳 2. Subindo o Ambiente de Desenvolvimento

O ambiente de desenvolvimento roda diretamente com:

```bash
docker-compose up -d --build
````

Ver logs:

```bash
docker-compose logs -f app
```

Acessar o TaskManager:

```
http://localhost:5000
```

---

# 🛢️ 3. Banco de Dados (PostgreSQL)

O banco é criado automaticamente com:

```
db/init.sql
```

Para acessar o banco:

```bash
docker exec -it modulo-05-compose-db-1 psql -U user -d taskdb
```

Ver tabelas:

```sql
\d tasks;
```

---

# ⚡ 4. Redis (Cache)

Testar o Redis:

```bash
docker exec -it modulo-05-compose-redis-1 redis-cli ping
```

Resultado esperado:

```
PONG
```

---

# ❤️ 5. Health Check

Testar health check da aplicação:

```
http://localhost/health
```

Saída:

```json
{
  "status": "healthy",
  "db": "ok",
  "redis": "ok",
  "version": "0.5.0",
  "environment": "development"
}
```

---

# 🌐 6. Ambiente de Produção (com NGINX + Réplicas)

Iniciar produção:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

Acessar:

```
http://localhost
```

Verificar réplicas:

```bash
docker ps
```

---

# 📁 7. Scripts de Automação

## Deploy

```bash
./scripts/deploy.sh
```

## Backup

```bash
./scripts/backup.sh
```

## Restore

```bash
./scripts/restore.sh
```

---

# 🛠 8. Troubleshooting

### Ver logs do app:

```bash
docker-compose logs app
```

### Ver logs do banco:

```bash
docker-compose logs db
```

### Ver containers:

```bash
docker ps -a
```

### Rebuild geral:

```bash
docker-compose build --no-cache
```

---

# 🎯 9. Conclusão do Módulo

Neste módulo, você evoluiu de um app simples (M03 e M04) para uma **arquitetura completa**, com:

* múltiplos serviços rodando juntos
* banco de dados persistente
* cache em memória (Redis)
* NGINX como reverse proxy
* múltiplas réplicas da aplicação
* health checks profissionais
* scripts de automação
* ambiente dev e ambiente prod separados

O projeto agora está preparado para:

* **Módulo 07 — CI/CD**
* **Módulo 08 — Observabilidade e Monitoramento**

---

# 📌 Próximos Passos

No próximo módulo, você aprenderá:

* pipelines
* automação de build
* testes
* deploy contínuo
* GitHub Actions

Prepare-se — agora começa o DevOps REAL.

