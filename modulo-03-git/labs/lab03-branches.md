# Lab 3 - Branches e Colaboração (45 minutos)

## Objetivo
Aprender a criar, trabalhar e mesclar branches sem gerar conflitos. Este lab mostra como usar o Git de forma profissional para desenvolver novas features com segurança.

## O que vamos fazer
1. Criar uma nova branch de feature
2. Adicionar endpoint de métricas para Prometheus
3. Fazer commits claros e organizados
4. Mesclar de volta na branch principal (main)

---

## Parte 1: Preparação do Ambiente (5 min)

### Passo 1.1 - Entrar no projeto

```bash
cd ~/devops-bootcamp/taskmanager-starter
```

---

### Passo 1.2 - Verificar status atual

```bash
git status
```

**Saída esperada:**
```
On branch main
nothing to commit, working tree clean
```

---

### Passo 1.3 - Ver branches existentes

```bash
git branch
```

**Você deve ver:**
```
* main
```

O asterisco indica a branch ativa.

---

### Passo 1.4 - Ativar ambiente virtual

```bash
source venv/bin/activate
```

**Checkpoint:** Prompt deve mostrar `(venv)` no início.

---

## Parte 2: Criando a Branch (10 min)

### Passo 2.1 - Criar e mudar para a nova branch

```bash
git checkout -b feature/metrics-endpoint
```

**Saída:**
```
Switched to a new branch 'feature/metrics-endpoint'
```

---

### Passo 2.2 - Confirmar mudança

```bash
git branch
```

**Você verá:**
```
  main
* feature/metrics-endpoint
```

O asterisco agora está na nova branch.

---

### Passo 2.3 - Entender o que aconteceu

```bash
# Ver histórico com branches
git log --oneline --graph --all
```

**Você verá** que ambas as branches (main e feature/metrics-endpoint) apontam para o mesmo commit.

---

## Parte 3: Criando o Endpoint de Métricas (20 min)

### Por que adicionar endpoint de métricas?

**Contexto DevOps:**
- Prometheus coleta métricas de aplicações
- Endpoint `/metrics` expõe dados em formato padrão
- Fundamental para observabilidade (Módulo 8)
- Permite monitorar performance em produção

---

### Passo 3.1 - Instalar biblioteca de métricas

```bash
pip install prometheus-client
```

**Aguarde a instalação.**

---

### Passo 3.2 - Atualizar requirements.txt

```bash
pip freeze > requirements.txt
```

**Verificar:**
```bash
cat requirements.txt | grep prometheus
```

Deve mostrar: `prometheus-client==0.X.X`

---

### Passo 3.3 - Adicionar endpoint de métricas no app.py

**Abra `app.py`** no VSCode.

**Adicione no início (após outros imports):**

```python
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Métricas Prometheus
requests_total = Counter('taskmanager_requests_total', 'Total de requisições', ['method', 'endpoint'])
request_duration = Histogram('taskmanager_request_duration_seconds', 'Duração das requisições')
```

**Adicione nova rota antes da linha `if __name__ == '__main__':`:**

```python
@app.route('/metrics')
def metrics():
    """Endpoint de métricas para Prometheus"""
    logger.debug("Métricas solicitadas")
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
```

**Modifique a rota `/` para contar requisições:**

```python
@app.route('/')
def index():
    requests_total.labels(method='GET', endpoint='/').inc()
    logger.info("Página inicial acessada")
    return """
    <h1>TaskManager v{}</h1>
    <p><strong>Ambiente:</strong> {}</p>
    <p><strong>Status:</strong> Operacional</p>
    <p><a href='/health'>Health Check</a> | <a href='/metrics'>Metrics</a></p>
    """.format(config.VERSION, config.ENVIRONMENT)
```

**Salve o arquivo** (`Ctrl + S`)

---

### Passo 3.4 - Testar o novo endpoint

```bash
# Rodar aplicação
python app.py
```

**Acesse no navegador:**
```
http://<ip-da-vm>:5000/metrics
```

**Você verá métricas no formato Prometheus:**
```
# HELP taskmanager_requests_total Total de requisições
# TYPE taskmanager_requests_total counter
taskmanager_requests_total{endpoint="/",method="GET"} 1.0
...
```

**Acesse a página inicial algumas vezes** e recarregue `/metrics` - o contador deve aumentar.

**Checkpoint:** Métricas funcionando corretamente.

**Pare a aplicação** (`Ctrl + C`)

---

## Parte 4: Commitando as Mudanças (10 min)

### Passo 4.1 - Ver o que mudou

```bash
git status
```

**Saída esperada:**
```
On branch feature/metrics-endpoint
Changes not staged for commit:
        modified:   app.py
        modified:   requirements.txt
```

---

### Passo 4.2 - Ver diferenças detalhadas

```bash
git diff
```

**Você verá:**
- Linhas removidas em vermelho (-)
- Linhas adicionadas em verde (+)

---

### Passo 4.3 - Adicionar mudanças

```bash
git add app.py requirements.txt
```

**Ou:**
```bash
git add .
```

---

### Passo 4.4 - Verificar staging area

```bash
git status
```

**Agora mostra:**
```
Changes to be committed:
        modified:   app.py
        modified:   requirements.txt
```

---

### Passo 4.5 - Fazer commit

```bash
git commit -m "adiciona endpoint /metrics para Prometheus"
```

**Saída:**
```
[feature/metrics-endpoint abc123d] adiciona endpoint /metrics para Prometheus
 2 files changed, 15 insertions(+), 1 deletion(-)
```

---

### Passo 4.6 - Ver histórico da branch

```bash
git log --oneline
```

**Você verá:**
```
abc123d (HEAD -> feature/metrics-endpoint) adiciona endpoint /metrics para Prometheus
def456g atualiza dependências com python-dotenv
...
```

---

## Parte 5: Mesclando com a Main (10 min)

### Passo 5.1 - Voltar para a branch principal

```bash
git checkout main
```

**Saída:**
```
Switched to branch 'main'
```

---

### Passo 5.2 - Verificar que mudanças não estão na main

**Abra `app.py`** - o endpoint `/metrics` NÃO está lá.

```bash
cat app.py | grep metrics
```

**Não retorna nada** - as mudanças estão apenas na branch de feature.

---

### Passo 5.3 - Mesclar a branch de feature

```bash
git merge feature/metrics-endpoint
```

**Saída (merge fast-forward):**
```
Updating def456g..abc123d
Fast-forward
 app.py            | 14 +++++++++++++-
 requirements.txt  |  1 +
 2 files changed, 14 insertions(+), 1 deletion(-)
```

---

### Passo 5.4 - Verificar que mudanças agora estão na main

```bash
cat app.py | grep metrics
```

**Agora retorna** as linhas com `/metrics`.

---

### Passo 5.5 - Ver histórico integrado

```bash
git log --oneline --graph --all
```

**Você verá:**
```
* abc123d (HEAD -> main, feature/metrics-endpoint) adiciona endpoint /metrics para Prometheus
* def456g atualiza dependências com python-dotenv
* xyz789e melhora health check com informações de versão e ambiente
...
```

Ambas as branches apontam para o mesmo commit agora.

---

### Passo 5.6 - Testar aplicação completa

```bash
source venv/bin/activate
python app.py
```

**Acesse:**
- http://ip-da-vm:5000 - Página inicial
- http://ip-da-vm:5000/health - Health check
- http://ip-da-vm:5000/metrics - Métricas (novo!)

**Tudo funcionando.**

**Pare com Ctrl + C**

---

### Passo 5.7 - Deletar a branch de feature (opcional)

```bash
git branch -d feature/metrics-endpoint
```

**Saída:**
```
Deleted branch feature/metrics-endpoint (was abc123d).
```

---

### Passo 5.8 - Ver branches restantes

```bash
git branch
```

**Agora só mostra:**
```
* main
```

**Nota:** O commit continua no histórico mesmo deletando a branch.

---

## Checkpoint Final

Ao final deste lab você deve ter:

- Branch `feature/metrics-endpoint` criada e mesclada
- Endpoint `/metrics` funcionando em produção
- Histórico Git limpo e organizado
- Nenhum conflito durante o merge
- Entendimento de workflow com branches

---

## Validação Completa

```bash
# 1. Verificar que está na main
git branch
# * main

# 2. Verificar histórico
git log --oneline -3

# 3. Verificar que mudanças estão presentes
grep -n "prometheus" app.py

# 4. Testar aplicação
python app.py &
sleep 2
curl http://localhost:5000/metrics | head -5
kill %1
```

---

## Problemas Comuns

### "error: Your local changes would be overwritten"

**Problema:** Tem mudanças não commitadas ao tentar mudar de branch

**Solução:**
```bash
# Commitar mudanças
git add .
git commit -m "sua mensagem"

# Ou guardar temporariamente
git stash
git checkout main
git stash pop
```

---

### "fatal: not a git repository"

**Problema:** Está fora da pasta do projeto

**Solução:**
```bash
# Verificar onde está
pwd

# Voltar para projeto
cd ~/devops-bootcamp/taskmanager-starter
```

---

### Endpoint /metrics não aparece

**Problema:** Não fez merge ou está na branch errada

**Solução:**
```bash
# Verificar branch atual
git branch

# Se não estiver na main, voltar
git checkout main

# Verificar se merge foi feito
git log --oneline | grep metrics
```

---

### "ModuleNotFoundError: prometheus_client"

**Problema:** Biblioteca não instalada

**Solução:**
```bash
source venv/bin/activate
pip install prometheus-client
```

---

### Merge deu conflito

**Problema:** Alguém modificou as mesmas linhas (raro neste lab)

**Solução:**
```bash
# Git marca conflitos assim:
<<<<<<< HEAD
código da main
=======
código da branch
>>>>>>> feature/metrics-endpoint

# 1. Abrir arquivo no VSCode
# 2. Escolher qual versão manter
# 3. Remover marcadores de conflito
# 4. Commitar
git add arquivo-com-conflito.py
git commit -m "resolve conflito de merge"
```

---

## Conceitos Aprendidos

### Branches
- Linha do tempo paralela de desenvolvimento
- Permite trabalhar sem afetar código estável
- Fundamental para trabalho em equipe
- Base de workflows profissionais

### Feature Branch
- Branch para desenvolver funcionalidade específica
- Nome descritivo (feature/nome-da-feature)
- Vida curta (horas ou dias, não semanas)
- Merge de volta quando pronta

### Merge Fast-Forward
- Tipo de merge mais simples
- Acontece quando não há divergência
- Main apenas "avança" para commit da branch
- Histórico linear

### Workflow DevOps
- Desenvolve em branch isolada
- Testa localmente
- Merge quando funcional
- Delete branch após merge

---

## Boas Práticas de Branches

### Nomenclatura
```bash
# Bom
feature/metrics-endpoint
feature/add-redis-cache
bugfix/health-check-timeout
hotfix/security-patch

# Ruim
nova-branch
teste
branch1
minha-branch
```

### Tamanho de Branch
- **Pequena:** 1 feature, algumas horas de trabalho
- **Média:** Feature complexa, 1-2 dias
- **Grande (evitar):** Múltiplas features, semanas

### Commits na Branch
```bash
# Bom - commits atômicos
git commit -m "adiciona biblioteca prometheus-client"
git commit -m "implementa endpoint /metrics"
git commit -m "adiciona contador de requisições"

# Ruim - commit gigante
git commit -m "adiciona métricas"
```

### Quando Criar Branch?
- **Criar:** Nova feature, refatoração grande, experimento
- **Não criar:** Fix de typo, ajuste de documentação, mudança de 1 linha

---

## Comparação: Com e Sem Branches

### Sem Branches (modo perigoso)
```bash
# Edita direto na main
vim app.py
git commit -m "tentando adicionar métricas"

# Quebrou algo? Main está quebrada para todos
# Precisa reverter? Afeta todo mundo
```

### Com Branches (modo seguro)
```bash
# Cria branch isolada
git checkout -b feature/metrics

# Experimenta livremente
vim app.py
git commit -m "adiciona métricas"

# Quebrou? Só sua branch está afetada
# Funcionou? Merge na main
git checkout main
git merge feature/metrics
```

---

## Visualizando Branches

### Comando básico
```bash
git log --oneline --graph --all
```

### Alias útil (configurar uma vez)
```bash
git config --global alias.lg "log --oneline --graph --all --decorate"

# Usar:
git lg
```

### Saída visual
```
* abc123d (HEAD -> main) adiciona endpoint /metrics
* def456g atualiza dependências
* xyz789e melhora health check
* a1b2c3d adiciona notas
```

---

## Próximo Lab

No **Lab 4** você vai aprender sobre **GitHub e Pull Requests**:
- Fazer fork de repositório da turma
- Configurar múltiplos remotes (origin e upstream)
- Abrir Pull Request real
- Participar de code review
- Sincronizar repositórios

Prepare-se para colaborar em equipe.

---

## Comandos de Referência

```bash
# Criar e mudar para branch
git checkout -b nome-branch

# Listar branches
git branch

# Mudar de branch
git checkout nome-branch

# Mesclar branch na atual
git merge nome-branch

# Deletar branch
git branch -d nome-branch

# Ver histórico visual
git log --oneline --graph --all
```

---

## Resumo do que Fizemos

1. Criamos branch `feature/metrics-endpoint`
2. Adicionamos endpoint `/metrics` para Prometheus
3. Commitamos mudanças na branch isolada
4. Mesclamos branch de volta na main
5. Deletamos branch após merge

**Você agora sabe:**
- Criar branches de feature
- Trabalhar isoladamente sem afetar main
- Fazer merge sem conflitos
- Usar workflow profissional de branches
- Adicionar observabilidade em aplicações

**Próximo passo:** Abra o **`lab04-github.md`** quando estiver pronto.