# Lab 2 - Configurações DevOps (45 minutos)

## Objetivo
Transformar o TaskManager em uma aplicação pronta para ambientes reais com configurações profissionais.

## O que vamos fazer
1. Criar variáveis de ambiente para configuração flexível
2. Melhorar o health check com informações úteis
3. Adicionar sistema de logs estruturado
4. Versionar tudo corretamente com múltiplos commits organizados

## Por que isso é importante

### Sem Configurações DevOps
- Senhas e secrets no código fonte
- Mesma configuração para dev e produção
- Difícil debugar problemas
- Impossível monitorar aplicação

### Com Configurações DevOps
- Secrets separados do código
- Ambientes diferentes (dev/staging/prod)
- Logs para troubleshooting
- Health checks para monitoramento
- Pronto para containerização (próximo módulo)

---

## Parte 1: Variáveis de Ambiente (15 min)

### Por que usar variáveis de ambiente?

**Ruim (hardcoded):**
```python
PORT = 5000
DEBUG = True
SECRET_KEY = "minha-senha-123"
```

**Bom (configurável):**
```python
PORT = os.getenv('PORT', '5000')
DEBUG = os.getenv('DEBUG', 'True')
SECRET_KEY = os.getenv('SECRET_KEY')
```

**Vantagens:**
- Mesma aplicação, múltiplos ambientes
- Secrets não vão para o Git
- Fácil mudar configuração sem editar código

---

### Passo 1.1 - Verificar ambiente

**No terminal do VSCode (conectado na VM):**

```bash
# Verificar que está no projeto correto
pwd
# Deve mostrar: /home/devops/devops-bootcamp/taskmanager-starter

# Ativar ambiente virtual se não estiver
source venv/bin/activate
```

---

### Passo 1.2 - Criar arquivo de configuração

**No VSCode**, crie novo arquivo: `config.py`

**Conteúdo completo:**

```python
import os

class Config:
    """Configuração base do TaskManager"""
    
    # Aplicação
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Servidor
    PORT = int(os.getenv('PORT', '5000'))
    HOST = os.getenv('HOST', '0.0.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Ambiente
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Versão
    VERSION = '0.1.0'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class DevelopmentConfig(Config):
    """Configurações específicas de desenvolvimento"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configurações específicas de produção"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'

# Mapeamento de ambientes
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retorna a configuração baseada no ambiente atual"""
    env = os.getenv('ENVIRONMENT', 'development')
    return config_map.get(env, config_map['default'])
```

**Salve o arquivo** (`Ctrl + S`)

---

### Passo 1.3 - Atualizar app.py

**Abra `app.py`** no VSCode.

**No início do arquivo (após os imports existentes), adicione:**

```python
import logging
from datetime import datetime
from config import get_config

# Carregar configuração
config = get_config()

# Configurar logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)
```

**Localize a linha `app = Flask(__name__)` e adicione logo abaixo:**

```python
app.config.from_object(config)
```

**No FINAL do arquivo, substitua a linha:**

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Por:**

```python
if __name__ == '__main__':
    logger.info(f"TaskManager v{config.VERSION} iniciando...")
    logger.info(f"Ambiente: {config.ENVIRONMENT}")
    logger.info(f"Servidor: http://{config.HOST}:{config.PORT}")
    
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )
```

**Salve o arquivo.**

---

### Passo 1.4 - Criar arquivo .env.example

**Criar arquivo `.env.example`:**

```bash
# Configurações do TaskManager
# Copie este arquivo para .env e ajuste os valores

# Ambiente de execução (development/production)
ENVIRONMENT=development

# Configurações do servidor
PORT=5000
HOST=0.0.0.0

# Debug (True/False)
DEBUG=True

# Nível de log (DEBUG/INFO/WARNING/ERROR/CRITICAL)
LOG_LEVEL=INFO

# Chave secreta (MUDE ISSO EM PRODUÇÃO!)
SECRET_KEY=dev-secret-key-change-in-production
```

**Salve o arquivo.**

---

### Passo 1.5 - Atualizar .gitignore

**Abra `.gitignore`** e adicione no topo:

```
# Environment Variables
.env
.env.local
.env.production
```

**Salve o arquivo.**

---

### Passo 1.6 - Testar configurações

```bash
# Rodar aplicação
python app.py
```

**Você deve ver logs melhorados:**
```
2025-XX-XX 10:30:15 - __main__ - INFO - TaskManager v0.1.0 iniciando...
2025-XX-XX 10:30:15 - __main__ - INFO - Ambiente: development
2025-XX-XX 10:30:15 - __main__ - INFO - Servidor: http://0.0.0.0:5000
 * Running on http://0.0.0.0:5000
```

**Configurações funcionando.**

**Pare a aplicação** (`Ctrl + C`)

---

## Parte 2: Health Check Profissional (10 min)

### Por que melhorar health check?

**Health check básico:**
```json
{"status": "ok"}
```

**Health check profissional:**
```json
{
  "status": "healthy",
  "service": "taskmanager",
  "version": "0.1.0",
  "environment": "development",
  "timestamp": "2025-01-15T10:30:00",
  "checks": {
    "app": "ok",
    "config": "loaded"
  }
}
```

**Vantagens:**
- Monitoramento sabe versão rodando
- Identifica ambiente rapidamente
- Timestamp para logs correlacionados
- Pode adicionar checks de banco/redis

---

### Passo 2.1 - Melhorar rota /health

**No `app.py`, localize a rota `/health` e substitua por:**

```python
@app.route('/health')
def health():
    """Health check endpoint para monitoramento"""
    health_status = {
        "status": "healthy",
        "service": "taskmanager",
        "version": config.VERSION,
        "environment": config.ENVIRONMENT,
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "app": "ok",
            "config": "loaded"
        }
    }
    logger.debug("Health check solicitado")
    return health_status
```

**Salve o arquivo.**

---

### Passo 2.2 - Testar health check

```bash
# Rodar aplicação
python app.py
```

**Em outro terminal (ou navegador), teste:**

```bash
# Abrir novo terminal no VSCode (botão + no terminal)
curl http://localhost:5000/health
```

**Ou acesse no navegador:**
```
http://<ip-da-vm>:5000/health
```

**Resposta esperada (JSON formatado):**
```json
{
  "status": "healthy",
  "service": "taskmanager",
  "version": "0.1.0",
  "environment": "development",
  "timestamp": "2025-01-15T10:35:22.123456",
  "checks": {
    "app": "ok",
    "config": "loaded"
  }
}
```

**Health check profissional funcionando.**

**Pare a aplicação** (`Ctrl + C`)

---

## Parte 3: Logs Estruturados (10 min)

### Por que adicionar logs?

**Sem logs:**
- Não sabe quando erro aconteceu
- Impossível debugar em produção
- Não rastreia uso da aplicação

**Com logs:**
- Sabe exatamente o que aconteceu
- Timestamp de cada operação
- Níveis (DEBUG, INFO, WARNING, ERROR)
- Facilita troubleshooting

---

### Passo 3.1 - Adicionar logs nas rotas

**No `app.py`, localize a rota `/` e modifique:**

```python
@app.route('/')
def index():
    logger.info("Página inicial acessada")
    return """
    <h1>TaskManager v{}</h1>
    <p><strong>Ambiente:</strong> {}</p>
    <p><strong>Status:</strong> Operacional</p>
    <p><a href='/health'>Health Check</a></p>
    """.format(config.VERSION, config.ENVIRONMENT)
```

**Salve o arquivo.**

---

### Passo 3.2 - Testar logs em ação

```bash
# Rodar aplicação
python app.py
```

**Acesse várias vezes no navegador:**
```
http://<ip-da-vm>:5000
```

**No terminal você verá:**
```
2025-XX-XX 10:40:15 - __main__ - INFO - Página inicial acessada
127.0.0.1 - - [15/Jan/2025 10:40:15] "GET / HTTP/1.1" 200 -
2025-XX-XX 10:40:18 - __main__ - INFO - Página inicial acessada
127.0.0.1 - - [15/Jan/2025 10:40:18] "GET / HTTP/1.1" 200 -
```

**Cada acesso é registrado com timestamp.**

---

### Passo 3.3 - Testar diferentes níveis de log

**Criar arquivo `.env` para testar:**

```bash
# Na raiz do projeto
echo "LOG_LEVEL=DEBUG" > .env
```

**Instalar python-dotenv:**
```bash
pip install python-dotenv
```

**No `app.py`, adicione no topo (após imports):**
```python
from dotenv import load_dotenv
load_dotenv()
```

**Rodar novamente:**
```bash
python app.py
```

**Agora você verá logs DEBUG também:**
```
2025-XX-XX 10:45:00 - __main__ - DEBUG - Health check solicitado
```

**Pare a aplicação** (`Ctrl + C`)

---

## Parte 4: Versionando com Commits Organizados (10 min)

### Por que múltiplos commits?

**Ruim (1 commit gigante):**
```
git commit -m "mudanças"
```

**Bom (commits atômicos):**
```
commit 3: adiciona logs estruturados
commit 2: melhora health check com métricas
commit 1: adiciona configuração via variáveis de ambiente
```

**Vantagens:**
- Histórico claro e legível
- Fácil reverter mudança específica
- Code review mais simples
- Rastreabilidade de bugs

---

### Passo 4.1 - Ver todas as mudanças

```bash
git status
```

**Você verá:**
```
Untracked files:
  .env
  .env.example
  config.py
  
Modified:
  .gitignore
  app.py
```

---

### Passo 4.2 - Commit 1 - Configurações

```bash
# Adicionar arquivos de configuração
git add config.py
git add .env.example
git add .gitignore

# Commitar
git commit -m "adiciona configuração via variáveis de ambiente"
```

**Saída:**
```
[main abc123d] adiciona configuração via variáveis de ambiente
 3 files changed, 45 insertions(+)
 create mode 100644 config.py
 create mode 100644 .env.example
```

---

### Passo 4.3 - Ver o que ainda falta commitar

```bash
git status
```

**Agora só resta:**
```
Modified:
  app.py
  
Untracked:
  .env
```

---

### Passo 4.4 - Commit 2 - Health Check

**Antes de commitar `app.py` completo, vamos ver as mudanças:**

```bash
git diff app.py
```

**Você verá em vermelho** (removido) **e verde** (adicionado) todas as mudanças.

**Commitar:**
```bash
git add app.py
git commit -m "melhora health check com informações de versão e ambiente"
```

---

### Passo 4.5 - Atualizar requirements.txt

**O arquivo `requirements.txt` precisa incluir python-dotenv:**

```bash
pip freeze > requirements.txt
```

**Verificar o arquivo:**
```bash
cat requirements.txt
```

Deve conter `python-dotenv==1.0.0`

---

### Passo 4.6 - Commit 3 - Dependencies

```bash
git add requirements.txt
git commit -m "atualiza dependências com python-dotenv"
```

---

### Passo 4.7 - Ver histórico completo

```bash
git log --oneline
```

**Saída esperada:**
```
def456g (HEAD -> main) atualiza dependências com python-dotenv
abc123d melhora health check com informações de versão e ambiente
xyz789e adiciona configuração via variáveis de ambiente
a1b2c3d adiciona notas de aprendizado e gitignore
...
```

**Histórico limpo e organizado.**

---

### Passo 4.8 - Ver detalhes de um commit

```bash
git show abc123d
```

**Mostra:**
- Autor e data
- Mensagem completa
- Todas as mudanças (diff)

---

## Parte 5: Teste Final com Ambientes Diferentes (5 min)

### Passo 5.1 - Testar ambiente de desenvolvimento

```bash
# Garantir que .env está configurado para dev
cat .env
```

Deve conter: `ENVIRONMENT=development`

```bash
python app.py
```

**Logs devem mostrar:**
```
Ambiente: development
```

**Pare com Ctrl + C**

---

### Passo 5.2 - Testar ambiente de produção

```bash
# Alterar temporariamente para produção
export ENVIRONMENT=production
export DEBUG=False
export LOG_LEVEL=WARNING

python app.py
```

**Logs devem mostrar:**
```
Ambiente: production
```

**Acesse health check** e veja `"environment": "production"`

**Pare com Ctrl + C**

---

### Passo 5.3 - Restaurar ambiente

```bash
# Remover variáveis exportadas
unset ENVIRONMENT
unset DEBUG
unset LOG_LEVEL
```

---

## Checkpoint Final

Ao final deste lab você deve ter:

- Configurações em variáveis de ambiente (config.py)
- Health check profissional com métricas
- Sistema de logs estruturado funcionando
- .env.example documentando variáveis
- .gitignore protegendo .env
- Múltiplos commits organizados (3+)
- Histórico Git limpo e legível

---

## Validação Completa

```bash
# 1. Verificar arquivos criados
ls -la | grep -E "config.py|.env.example"

# 2. Verificar histórico de commits
git log --oneline -3

# 3. Verificar que .env não está no Git
git status
# Não deve mostrar .env na lista

# 4. Testar aplicação
python app.py
# Deve iniciar com logs estruturados

# 5. Testar health check (outro terminal)
curl http://localhost:5000/health | python -m json.tool
```

---

## Problemas Comuns

### "ModuleNotFoundError: No module named 'config'"

**Problema:** Arquivo `config.py` não foi salvo ou está em pasta errada

**Solução:**
```bash
# Verificar se arquivo existe
ls -la config.py

# Deve estar na raiz do projeto
pwd
# /home/devops/devops-bootcamp/taskmanager-starter
```

---

### "ModuleNotFoundError: No module named 'dotenv'"

**Problema:** python-dotenv não instalado

**Solução:**
```bash
source venv/bin/activate
pip install python-dotenv
pip freeze > requirements.txt
```

---

### Variáveis de ambiente não funcionam

**Problema:** Variáveis exportadas com `export` não persistem

**Solução 1 - Usar arquivo .env:**
```bash
# Criar .env
echo "ENVIRONMENT=production" > .env
echo "LOG_LEVEL=WARNING" >> .env

# python-dotenv carrega automaticamente
python app.py
```

**Solução 2 - Exportar na mesma linha:**
```bash
ENVIRONMENT=production DEBUG=False python app.py
```

---

### Logs não aparecem no nível esperado

**Problema:** LOG_LEVEL configurado errado

**Solução:**
```bash
# Verificar valor
echo $LOG_LEVEL

# Ou testar explicitamente
LOG_LEVEL=DEBUG python app.py
```

---

### Git mostra .env como untracked

**Problema:** .gitignore não funcionando

**Solução:**
```bash
# Verificar conteúdo do .gitignore
cat .gitignore | grep .env

# Se .env já foi commitado antes, remover:
git rm --cached .env
git commit -m "remove .env do versionamento"
```

---

### Aplicação não carrega configurações

**Problema:** Esqueceu de importar ou chamar get_config()

**Solução:**
```python
# No app.py, verificar se tem:
from config import get_config
config = get_config()
```

---

## Conceitos Aprendidos

### Variáveis de Ambiente
- Separam configuração de código
- Permitem múltiplos ambientes (dev/prod)
- Protegem secrets e senhas
- Padrão da indústria (12-factor app)

### Health Checks
- Endpoint para monitoramento externo
- Kubernetes/Docker usam para liveness probe
- Deve retornar status + metadados úteis
- Fundamental para observabilidade

### Logging Estruturado
- Níveis: DEBUG < INFO < WARNING < ERROR < CRITICAL
- Timestamp automático
- Facilita troubleshooting
- Essencial para produção

### Commits Atômicos
- Um commit = uma mudança lógica
- Mensagens descritivas
- Histórico navegável
- Facilita code review e rollback

---

## Boas Práticas Aprendidas

### Configuração
```python
# Bom
PORT = int(os.getenv('PORT', '5000'))

# Ruim
PORT = 5000
```

### Secrets
```bash
# Bom - .env (não commitado)
SECRET_KEY=prod-key-xyz

# Ruim - hardcoded
SECRET_KEY = "minha-senha-123"
```

### Logs
```python
# Bom
logger.info("Usuário X fez login")

# Ruim
print("login")
```

### Commits
```bash
# Bom
git commit -m "adiciona rate limiting na API"

# Ruim
git commit -m "fix"
```

---

## Dicas Profissionais

### Para Desenvolvimento
```bash
# .env para dev
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
```

### Para Produção
```bash
# .env para prod
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
SECRET_KEY=<chave-super-secreta>
```

### Testando Localmente
```bash
# Testar como se fosse produção
ENVIRONMENT=production DEBUG=False python app.py
```

### Verificando Configuração
```python
# Adicionar rota /config (apenas dev!)
@app.route('/config')
def show_config():
    if config.ENVIRONMENT != 'development':
        return "Not available in production", 403
    return {k: str(v) for k, v in config.__dict__.items()}
```

---

## Próximo Lab

No **Lab 3** você vai aprender sobre **branches**:
- Criar branches de feature
- Desenvolver mudanças isoladamente
- Fazer merge sem conflitos
- Simular workflow de equipe profissional

Prepare-se para trabalhar como em empresas reais.

---

## Resumo do que Fizemos

1. Criamos config.py para configuração flexível
2. Melhoramos health check com metadados úteis
3. Implementamos logging estruturado
4. Protegemos secrets com .env e .gitignore
5. Fizemos múltiplos commits organizados

**Você agora sabe:**
- Configurar aplicações com variáveis de ambiente
- Implementar health checks profissionais
- Usar logging para troubleshooting
- Proteger informações sensíveis
- Versionar mudanças de forma organizada

**Próximo passo:** Abra o **`lab03-branches.md`** quando estiver pronto.