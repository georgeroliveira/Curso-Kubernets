# TaskManager - Módulo 05 - Docker Compose

Sistema completo de gerenciamento de tarefas com arquitetura multi-container, alta disponibilidade e pronto para produção.

## Stack Tecnológica

| Tecnologia | Versão | Função |
|------------|--------|--------|
| Python Flask | 2.3+ | Aplicação web |
| PostgreSQL | 15 | Banco de dados |
| Redis | 7 | Cache e sessões |
| Nginx | Alpine | Load balancer |
| Docker Compose | 3.8+ | Orquestração |

## Arquitetura

```
Internet → Nginx → [App1, App2, App3] → [PostgreSQL, Redis]
```

- **3 instâncias** da aplicação (alta disponibilidade)
- **Nginx** como proxy reverso e load balancer
- **PostgreSQL** para dados persistentes
- **Redis** para cache e sessões
- **Redes isoladas** (frontend/backend)
- **Health checks** automáticos
- **Auto-restart** em caso de falhas

## Quick Start

### Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- Git
- 4GB RAM livre
- 10GB disco livre

### Instalação

**1. Clonar repositório:**
```bash
# Linux/Mac
git clone https://github.com/seu-usuario/taskmanager.git
cd taskmanager/modulo-05-compose

# Windows PowerShell
git clone https://github.com/seu-usuario/taskmanager.git
Set-Location taskmanager\modulo-05-compose
```

**2. Configurar variáveis de ambiente:**
```bash
# Linux/Mac
cp .env.example .env
nano .env  # Editar e trocar senhas

# Windows PowerShell
Copy-Item .env.example .env
notepad .env  # Editar e trocar senhas
```

**3. Subir a stack:**
```bash
docker-compose up -d
```

**4. Verificar status:**
```bash
docker-compose ps
```

**5. Acessar aplicação:**
```
http://localhost
```

## Estrutura do Projeto

```
modulo-05-compose/
├── README.md                      # Este arquivo
├── docker-compose.yml             # Configuração principal
├── docker-compose.prod.yml        # Override para produção
├── .env.example                   # Template de variáveis
├── .env                           # Variáveis (não commitado)
├── .gitignore
│
├── taskmanager/                   # Código da aplicação
│   ├── app.py                     # Aplicação Flask
│   ├── logger.py                  # Logging estruturado
│   ├── Dockerfile                 # Imagem Docker
│   ├── requirements.txt           # Dependências Python
│   └── templates/                 # Templates HTML
│       └── index.html
│
├── config/                        # Configurações
│   └── init.sql                   # Script inicialização DB
│
├── nginx/                         # Configuração Nginx
│   └── nginx.conf                 # Load balancer config
│
├── scripts/                       # Scripts de automação
│   ├── deploy.sh                  # Deploy automatizado
│   ├── backup.sh                  # Backup do banco
│   ├── restore.sh                 # Restore do banco
│   └── health-check.sh            # Verificação de saúde
│
├── logs/                          # Logs (gitignored)
│   ├── app1/
│   ├── app2/
│   ├── app3/
│   └── nginx/
│
├── backups/                       # Backups (gitignored)
│   └── taskmanager_*.sql.gz
│
├── labs/                          # Laboratórios práticos
│   ├── lab01-stack-multi-container.md
│   ├── lab02-nginx-escalabilidade.md
│   └── lab03-producao-ready.md
│
└── docs/                          # Documentação
    ├── troubleshooting.md         # Guia de problemas
    ├── comandos-cheatsheet.md     # Comandos úteis
    └── arquitetura.md             # Arquitetura detalhada
```

## Comandos Principais

### Gerenciamento Básico

```bash
# Subir todos os serviços
docker-compose up -d

# Ver status
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Parar serviços
docker-compose stop

# Parar e remover
docker-compose down

# Restart
docker-compose restart
```

### Operações Específicas

```bash
# Deploy completo
./scripts/deploy.sh

# Backup do banco
./scripts/backup.sh

# Restore do banco
./scripts/restore.sh

# Health check de todos os serviços
curl http://localhost/health | jq '.'

# Ver qual instância está respondendo
for i in {1..10}; do
  curl -s http://localhost/health | jq -r '.instance.id'
done
```

### Debug e Troubleshooting

```bash
# Logs de serviço específico
docker-compose logs app1
docker-compose logs db
docker-compose logs nginx

# Executar comando em container
docker-compose exec app1 sh
docker-compose exec db psql -U taskuser -d taskdb

# Ver uso de recursos
docker stats

# Rebuild sem cache
docker-compose build --no-cache

# Ver configuração processada
docker-compose config
```

## Serviços e Portas

| Serviço | Porta | URL | Descrição |
|---------|-------|-----|-----------|
| **Nginx** | 80 | http://localhost | Proxy reverso |
| **App1/2/3** | 5000 | Interno | Aplicação Flask |
| **PostgreSQL** | 5432 | Interno (dev: exposto) | Banco de dados |
| **Redis** | 6379 | Interno | Cache |

**NOTA:** Em produção, apenas Nginx (porta 80) é exposto externamente.

## Variáveis de Ambiente

Principais variáveis no `.env`:

```bash
# Database
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpass123

# Redis
REDIS_PASSWORD=redis123

# Application
FLASK_ENV=production
SECRET_KEY=change-this-in-production

# Ports
APP_PORT=5000
DB_PORT=5432
REDIS_PORT=6379
```

Ver `.env.example` para lista completa.

## Backup e Restore

### Backup Automático

```bash
# Executar backup manual
./scripts/backup.sh

# Configurar backup diário (cron)
# Linux/Mac - adicionar ao crontab:
0 2 * * * cd /opt/taskmanager && ./scripts/backup.sh
```

**Backups são salvos em:** `./backups/taskmanager_YYYYMMDD_HHMMSS.sql.gz`

**Retenção:** 7 dias (automático)

### Restore

```bash
# Executar restore interativo
./scripts/restore.sh

# Listar backups disponíveis
ls -lh backups/

# Restore manual
gunzip -c backups/taskmanager_20251013_020000.sql.gz | \
  docker-compose exec -T db psql -U taskuser -d taskdb
```

## Próximos Módulos

### Módulo 06 - Infrastructure as Code
- Provisionar VMs com Terraform
- Automatizar deploy com Ansible
- Gerenciar múltiplos ambientes

### Módulo 07 - CI/CD Pipelines
- GitHub Actions / GitLab CI
- Testes automatizados
- Deploy automatizado

### Módulo 08 - Observabilidade
- Prometheus + Grafana
- Logs centralizados com Loki
- Alertas e dashboards

## Recursos Adicionais

### Documentação

- [Labs Práticos](labs/) - Exercícios hands-on
- [Troubleshooting Guide](docs/troubleshooting.md) - Problemas e soluções
- [Comandos Cheat Sheet](docs/comandos-cheatsheet.md) - Comandos úteis
- [Arquitetura Detalhada](docs/arquitetura.md) - Diagramas e explicações

### Links Úteis

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Redis Docker](https://hub.docker.com/_/redis)
- [Nginx Docker](https://hub.docker.com/_/nginx)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Licença

MIT License - ver arquivo LICENSE

## Suporte

- **Discord:** [Link do Discord do curso]
- **Email:** suporte@cursosdevops.com
- **Issues:** GitHub Issues
- **Documentação:** Este README + `/docs`

---

**Desenvolvido com dedicação para o Curso DevOps Essencial**

**Versão:** 1.0.0  
**Última atualização:** Outubro 2025  
**Compatível com:** Docker 20.10+, Docker Compose 2.0+