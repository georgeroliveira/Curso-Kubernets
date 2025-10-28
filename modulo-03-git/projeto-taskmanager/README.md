# TaskManager - Sistema de Gerenciamento de Tarefas

Projeto desenvolvido durante o DevOps Bootcamp 2025 para ensinar práticas modernas de DevOps.

## Sobre o Projeto

TaskManager é uma aplicação web simples de gerenciamento de tarefas (to-do list) construída com Flask. O projeto evolui ao longo dos módulos do bootcamp, incorporando práticas e ferramentas DevOps progressivamente.

## Tecnologias

- **Backend:** Python 3.12 + Flask 2.3
- **Frontend:** HTML5 + CSS3
- **Servidor:** Gunicorn (produção)
- **Ambiente:** Ubuntu 24.04 LTS

## Evolução do Projeto

### Módulo 3 - Git e Versionamento
- Configuração via variáveis de ambiente
- Health checks profissionais
- Sistema de logs estruturado
- API REST básica
- Endpoint de métricas Prometheus

### Módulo 4 - Docker (próximo)
- Containerização da aplicação
- Dockerfile otimizado
- Docker Compose

### Módulo 5 - Persistência
- PostgreSQL
- Redis para cache
- Nginx como proxy reverso

### Módulo 6 - Infraestrutura como Código
- Ansible playbooks
- Provisionamento automatizado

### Módulo 7 - CI/CD
- Pipeline GitHub Actions
- Deploy automatizado
- Testes automatizados

### Módulo 8 - Observabilidade
- Prometheus + Grafana
- Logs centralizados
- Alertas

## Pré-requisitos

- Python 3.8 ou superior
- pip
- virtualenv (recomendado)

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/taskmanager.git
cd taskmanager
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite .env com suas configurações
```

### 5. Executar aplicação

**Desenvolvimento:**
```bash
python app.py
```

**Produção:**
```bash
gunicorn -b 0.0.0.0:8080 app:app
```

## Uso

### Acessar aplicação

```
http://localhost:5000
```

### Endpoints disponíveis

- `GET /` - Interface web principal
- `GET /health` - Health check para monitoramento
- `GET /metrics` - Métricas Prometheus
- `GET /api/tasks` - Listar todas as tarefas (JSON)
- `POST /api/tasks` - Criar nova tarefa (JSON)
- `PUT /api/tasks/<id>` - Atualizar tarefa (JSON)
- `DELETE /api/tasks/<id>` - Deletar tarefa (JSON)

## Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão | Obrigatória |
|----------|-----------|--------|-------------|
| `ENVIRONMENT` | Ambiente de execução | development | Não |
| `PORT` | Porta do servidor | 5000 | Não |
| `HOST` | IP de bind | 0.0.0.0 | Não |
| `DEBUG` | Modo debug | True | Não |
| `LOG_LEVEL` | Nível de log | INFO | Não |
| `SECRET_KEY` | Chave secreta Flask | auto | Sim (prod) |

### Exemplo .env

```bash
ENVIRONMENT=development
PORT=5000
DEBUG=True
LOG_LEVEL=DEBUG
SECRET_KEY=dev-secret-key
```

## Health Check

Verificar se a aplicação está saudável:

```bash
curl http://localhost:5000/health
```

Resposta esperada:

```json
{
  "status": "healthy",
  "service": "taskmanager",
  "version": "0.1.0",
  "environment": "development",
  "timestamp": "2025-01-15T10:30:00.123456",
  "checks": {
    "app": "ok",
    "config": "loaded",
    "tasks_count": 0
  }
}
```

## Métricas

Endpoint Prometheus para observabilidade:

```bash
curl http://localhost:5000/metrics
```

Métricas disponíveis:
- `taskmanager_requests_total` - Total de requisições por endpoint
- `taskmanager_request_duration_seconds` - Duração das requisições

## API REST

### Listar tarefas

```bash
curl http://localhost:5000/api/tasks
```

### Criar tarefa

```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Minha nova tarefa"}'
```

### Atualizar tarefa

```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Deletar tarefa

```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

## Estrutura do Projeto

```
taskmanager/
├── app.py              # Aplicação Flask principal
├── config.py           # Configurações por ambiente
├── requirements.txt    # Dependências Python
├── VERSION             # Versão da aplicação
├── .env.example        # Exemplo de variáveis de ambiente
├── .gitignore          # Arquivos ignorados pelo Git
├── .dockerignore       # Arquivos ignorados pelo Docker
├── static/
│   └── style.css       # Estilos CSS
├── templates/
│   └── index.html      # Template HTML principal
└── README.md           # Este arquivo
```

## Desenvolvimento

### Executar em modo debug

```bash
export DEBUG=True
export LOG_LEVEL=DEBUG
python app.py
```

### Logs

Logs são exibidos no console com formato estruturado:

```
2025-01-15 10:30:00 - __main__ - INFO - TaskManager v0.1.0 iniciando...
2025-01-15 10:30:00 - __main__ - INFO - Ambiente: development
2025-01-15 10:30:00 - __main__ - INFO - Servidor: http://0.0.0.0:5000
```

## Testes

(Será implementado no Módulo 7)

```bash
pytest tests/
```

## Deploy

### Desenvolvimento

```bash
python app.py
```

### Produção com Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

Onde:
- `-w 4` - 4 workers (ajuste conforme CPU)
- `-b 0.0.0.0:8080` - Bind em todas interfaces, porta 8080

## Troubleshooting

### Porta já em uso

```bash
# Verificar processo usando a porta
lsof -i :5000

# Matar processo
kill -9 <PID>
```

### ModuleNotFoundError

```bash
# Verificar ambiente virtual ativo
which python

# Reinstalar dependências
pip install -r requirements.txt
```

### Variáveis de ambiente não carregam

```bash
# Verificar se .env existe
ls -la .env

# Verificar python-dotenv instalado
pip list | grep dotenv
```

## Segurança

### Checklist de Produção

- Definir SECRET_KEY única e forte
- Desabilitar DEBUG (DEBUG=False)
- Usar HTTPS (configurar no Nginx/proxy)
- Não commitar arquivo .env
- Atualizar dependências regularmente
- Limitar acesso às portas (firewall)

### Atualizar dependências

```bash
pip list --outdated
pip install -U <pacote>
pip freeze > requirements.txt
```

## Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto é material educacional do DevOps Bootcamp 2025.

## Contato

- Instrutor: DevOps Bootcamp Team
- Issues: GitHub Issues do repositório

## Roadmap

- [x] Módulo 3 - Versionamento com Git
- [ ] Módulo 4 - Containerização com Docker
- [ ] Módulo 5 - Orquestração multi-container
- [ ] Módulo 6 - Infraestrutura como Código
- [ ] Módulo 7 - Pipeline CI/CD
- [ ] Módulo 8 - Observabilidade completa

---

**Versão:** 0.1.0  
**Última atualização:** 2025  
**Módulo atual:** 3 - Git e Versionamento