# Lab 1 - Setup e Exploração (30 minutos)

## Objetivo
Conectar no servidor via Remote SSH, configurar Git na VM e explorar seu primeiro projeto DevOps — o TaskManager.

## O que vamos fazer
1. Conectar VSCode na VM via Remote SSH
2. Configurar Git no servidor
3. Clonar o projeto TaskManager
4. Explorar a estrutura do código
5. Fazer seu primeiro commit

---

## Parte 1: Conectando no Servidor (5 min)

### Passo 1.1 - Descobrir o IP da VM

**Na VM Ubuntu** (via terminal direto ou console do virtualizador):
```bash
hostname -I
```

**Anote o IP** (exemplo: `192.168.64.5` ou `10.0.2.15`)

---

### Passo 1.2 - Abrir VSCode e Conectar

**No seu computador local:**

1. Abra o VSCode
2. Pressione: `Ctrl + Shift + P`
3. Digite: `Remote-SSH: Connect to Host`
4. Digite: `devops@<ip-da-vm>` (substitua pelo IP real)
5. Selecione **Linux** como tipo de sistema
6. Digite a senha quando solicitado

**Validação:**
- Canto inferior esquerdo deve mostrar: `SSH: <ip-da-vm>`
- Terminal integrado deve estar conectado na VM

---

### Passo 1.3 - Abrir Terminal Integrado

**No VSCode:**
- Atalho: `Ctrl + J`

**Você verá algo como:**
```
devops@ubuntu:~$
```

**Checkpoint:** Se vê esse prompt, está conectado na VM corretamente.

---

## Parte 2: Configurando o Git (5 min)

Todos os comandos a partir daqui são **dentro do terminal do VSCode** (que está conectado na VM).

### Passo 2.1 - Configurar identidade

```bash
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu.email@exemplo.com"
```

**Importante:** Use o **mesmo email** cadastrado no GitHub.

---

### Passo 2.2 - Verificar configuração

```bash
git config --list
```

**Saída esperada:**
```
user.name=Seu Nome Completo
user.email=seu.email@exemplo.com
...
```

---

### Passo 2.3 - Configurar editor padrão (opcional)

```bash
git config --global core.editor "nano"
```

Isso evita que Git abra o `vim` (difícil para iniciantes).

---

### Passo 2.4 - Criar pasta de trabalho

```bash
cd ~
mkdir -p devops-bootcamp
cd devops-bootcamp
pwd
```

**Saída esperada:**
```
/home/devops/devops-bootcamp
```

**Checkpoint:** Você está na pasta correta para trabalhar.

---

## Parte 3: Clonando o Projeto (5 min)

### Passo 3.1 - Clonar o repositório inicial

```bash
git clone https://github.com/devops-bootcamp/taskmanager-starter.git
```

**Saída esperada:**
```
Cloning into 'taskmanager-starter'...
remote: Enumerating objects: ...
Receiving objects: 100% ...
```

**Nota para o Instrutor:** O repositório `devops-bootcamp/taskmanager-starter` deve existir e estar público antes da aula.

---

### Passo 3.2 - Entrar na pasta do projeto

```bash
cd taskmanager-starter
```

---

### Passo 3.3 - Ver estrutura do projeto

```bash
ls -la
```

**Você deve ver:**
```
.git/                  # Pasta do Git (controle de versão)
app.py                 # Código principal da aplicação
requirements.txt       # Dependências Python
README.md              # Documentação
```

---

### Passo 3.4 - Ver status do Git

```bash
git status
```

**Saída esperada:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Checkpoint:** Git está funcionando e não há mudanças pendentes.

---

## Parte 4: Explorando o Projeto (8 min)

### Passo 4.1 - Abrir pasta no VSCode

**No terminal integrado:**
```bash
code .
```

Ou use o menu: **File > Open Folder** e navegue até `/home/devops/devops-bootcamp/taskmanager-starter`

---

### Passo 4.2 - Examinar app.py

Abra o arquivo `app.py` no VSCode e observe:

**Estrutura básica:**
- Importação do Flask
- Rota `/` (página inicial)
- Rota `/health` (health check)
- Servidor rodando na porta 5000

**Você NÃO precisa entender todo o código Python.** Foque em:
- Onde estão as rotas (linhas com `@app.route`)
- Como o servidor é iniciado (final do arquivo)

---

### Passo 4.3 - Examinar requirements.txt

```bash
cat requirements.txt
```

**Conteúdo:**
```
Flask==2.3.3
python-dotenv==1.0.0
gunicorn==21.2.0
Werkzeug==2.3.7
```

Essas são as bibliotecas Python que a aplicação precisa.

---

### Passo 4.4 - Ver histórico do repositório

```bash
git log --oneline
```

**Você verá os commits iniciais** feitos pelo instrutor ao preparar o projeto.

---

## Parte 5: Testando a Aplicação (5 min)

### Passo 5.1 - Criar ambiente virtual Python

```bash
python3 -m venv venv
```

Aguarde alguns segundos enquanto o ambiente é criado.

---

### Passo 5.2 - Ativar ambiente virtual

```bash
source venv/bin/activate
```

**Validação:** O prompt deve mudar para:
```
(venv) devops@ubuntu:~/devops-bootcamp/taskmanager-starter$
```

O `(venv)` indica que o ambiente virtual está ativo.

---

### Passo 5.3 - Instalar dependências

```bash
pip install -r requirements.txt
```

**Aguarde a instalação** (pode levar 30-60 segundos).

**Saída esperada ao final:**
```
Successfully installed Flask-2.3.3 Werkzeug-2.3.7 ...
```

---

### Passo 5.4 - Executar a aplicação

```bash
python app.py
```

**Saída esperada:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://0.0.0.0:5000
```

**A aplicação está rodando.**

---

### Passo 5.5 - Testar no navegador

**No seu computador local**, abra o navegador e acesse:

```
http://<ip-da-vm>:5000
```

**Exemplo:**
```
http://192.168.64.5:5000
```

**Você deve ver:**
- Página inicial do TaskManager
- Título "TaskManager"
- Link para `/health`

---

### Passo 5.6 - Testar health check

Acesse no navegador:
```
http://<ip-da-vm>:5000/health
```

**Você deve ver JSON:**
```json
{
  "status": "healthy",
  "service": "taskmanager"
}
```

**Checkpoint:** Aplicação funciona corretamente.

---

### Passo 5.7 - Parar a aplicação

**No terminal do VSCode**, pressione:
```
Ctrl + C
```

A aplicação para de rodar.

---

## Parte 6: Seu Primeiro Commit (7 min)

### Passo 6.1 - Criar arquivo de anotações

**No VSCode**, crie novo arquivo: `NOTAS.md`

**Conteúdo:**
```markdown
# Minhas Notas - DevOps Bootcamp

## Data
2025-XX-XX

## O que aprendi hoje

### Git
- Git versiona código e configurações
- Clone baixa repositório remoto
- Status mostra mudanças pendentes
- Commit salva "foto" do projeto

### TaskManager
- Aplicação Flask simples
- Roda na porta 5000
- Tem health check em /health
- Usa ambiente virtual Python

### Remote SSH
- Edito no VSCode local
- Arquivos estão na VM
- Git roda dentro da VM

## Próximos passos
- Adicionar configurações DevOps
- Aprender sobre branches
- Fazer Pull Request no GitHub

## Dúvidas
(Anote suas dúvidas aqui durante a aula)
```

**Salve o arquivo** (`Ctrl + S`)

---

### Passo 6.2 - Ver o que mudou

```bash
git status
```

**Saída esperada:**
```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        NOTAS.md
        venv/

nothing added to commit but untracked files present
```

**Explicação:**
- `NOTAS.md` - Arquivo novo (não rastreado)
- `venv/` - Ambiente virtual (não devemos versionar)

---

### Passo 6.3 - Criar .gitignore

**Criar arquivo `.gitignore`** no VSCode:

```
# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd

# Environment
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

**Salve o arquivo.**

---

### Passo 6.4 - Verificar status novamente

```bash
git status
```

**Agora você verá:**
```
Untracked files:
        .gitignore
        NOTAS.md
```

O `venv/` sumiu da lista. O `.gitignore` está funcionando.

---

### Passo 6.5 - Adicionar arquivos ao Git

```bash
git add NOTAS.md
git add .gitignore
```

**Ou adicionar tudo de uma vez:**
```bash
git add .
```

---

### Passo 6.6 - Verificar staging area

```bash
git status
```

**Saída esperada:**
```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .gitignore
        new file:   NOTAS.md
```

**Explicação:** Arquivos estão na "staging area" (prontos para commit).

---

### Passo 6.7 - Fazer o commit

```bash
git commit -m "adiciona notas de aprendizado e gitignore"
```

**Saída esperada:**
```
[main a1b2c3d] adiciona notas de aprendizado e gitignore
 2 files changed, 25 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 NOTAS.md
```

**Seu primeiro commit foi criado.**

---

### Passo 6.8 - Ver o histórico

```bash
git log --oneline
```

**Você verá:**
```
a1b2c3d (HEAD -> main) adiciona notas de aprendizado e gitignore
f9e8d7c commit inicial do projeto
...
```

O commit mais recente (seu) aparece no topo.

---

### Passo 6.9 - Ver detalhes do commit

```bash
git show
```

**Mostra:**
- Hash do commit
- Autor e data
- Mensagem
- Diferenças (diff) dos arquivos

---

## Checkpoint Final

Ao final deste lab você deve ter:

- VSCode conectado na VM via Remote SSH
- Git configurado com seu nome e email
- Projeto TaskManager clonado dentro da VM
- Aplicação testada e funcionando (http://ip-da-vm:5000)
- Primeiro commit realizado com sucesso
- .gitignore configurado corretamente

---

## Validação Completa

Execute os comandos abaixo para verificar tudo:

```bash
# 1. Verificar Git configurado
git config --global user.name
git config --global user.email

# 2. Verificar que está no projeto correto
pwd
# Deve mostrar: /home/devops/devops-bootcamp/taskmanager-starter

# 3. Verificar histórico de commits
git log --oneline

# 4. Verificar que não há mudanças pendentes
git status
# Deve mostrar: "working tree clean"
```

---

## Problemas Comuns

### "Could not resolve hostname"

**Problema:** IP da VM está errado

**Solução:**
```bash
# Na VM (console direto)
hostname -I
```
Use o IP correto ao conectar.

---

### "Permission denied (publickey)"

**Problema:** VSCode tentando usar SSH key em vez de senha

**Solução:**
- Adicione senha quando solicitado
- Ou configure SSH keys (já deve ter sido feito no Módulo 2)

---

### "git: command not found"

**Problema:** Git não instalado na VM

**Solução:**
```bash
sudo apt update
sudo apt install git -y
```

---

### "pip: command not found"

**Problema:** Python/pip não instalado

**Solução:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
```

---

### "Connection refused" ao acessar http://ip-da-vm:5000

**Problema:** Firewall bloqueando porta ou aplicação não rodando

**Solução 1 - Verificar se app está rodando:**
```bash
# Na VM
python app.py
# Deve mostrar: Running on http://0.0.0.0:5000
```

**Solução 2 - Abrir porta no firewall:**
```bash
sudo ufw allow 5000/tcp
```

**Solução 3 - Testar localmente na VM:**
```bash
curl http://localhost:5000
```
Se funciona localmente mas não remotamente, é problema de rede/firewall.

---

### "fatal: not a git repository"

**Problema:** Está fora da pasta do projeto

**Solução:**
```bash
cd ~/devops-bootcamp/taskmanager-starter
git status
```

---

### Ambiente virtual não ativa

**Problema:** Comando `source venv/bin/activate` não funcionou

**Solução:**
```bash
# Recriar ambiente virtual
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

---

## Conceitos Aprendidos

### Remote SSH
- Editar arquivos remotamente como se fossem locais
- Terminal integrado roda comandos na VM
- Simula trabalho profissional em servidores

### Git Básico
- **Repository:** Pasta com histórico versionado (.git)
- **Status:** Ver mudanças pendentes
- **Add:** Preparar arquivos para commit (staging)
- **Commit:** Salvar snapshot do projeto
- **Log:** Ver histórico de commits

### .gitignore
- Previne arquivos desnecessários de serem versionados
- Evita expor secrets (senhas, tokens)
- Reduz tamanho do repositório

### Ambiente Virtual Python
- Isola dependências do projeto
- Evita conflitos entre projetos
- Boa prática em desenvolvimento Python

---

## Dicas Profissionais

### Fluxo de Trabalho
1. **Sempre use `git status`** antes de qualquer operação
2. **Commits frequentes** são melhores que um commit gigante
3. **Mensagens claras** facilitam debug futuro
4. **Teste antes de commitar** para não quebrar o projeto

### Comandos Úteis
```bash
# Ver diferenças antes de commitar
git diff

# Ver histórico visual
git log --oneline --graph

# Desfazer mudanças não commitadas
git checkout -- arquivo.py
```

### Atalhos VSCode
- `Ctrl + J` - Abrir/fechar terminal
- `Ctrl + P` - Buscar arquivos rapidamente
- `Ctrl + Shift + P` - Command Palette (todos os comandos)

---

## Próximo Lab

No **Lab 2** você vai transformar o TaskManager em uma aplicação pronta para produção:
- Adicionar variáveis de ambiente
- Implementar health check robusto
- Configurar logs profissionais
- Fazer múltiplos commits organizados

Prepare-se para aplicar DevOps de verdade.

---

## Resumo do que Fizemos

1. Conectamos VSCode na VM
2. Configuramos Git com nossa identidade
3. Clonamos projeto do GitHub
4. Testamos aplicação rodando
5. Criamos primeiro commit

**Você agora sabe:**
- Trabalhar remotamente via SSH
- Usar Git para versionar código
- Clonar repositórios
- Fazer commits
- Usar .gitignore

**Próximo passo:** Abra o **`lab02-config.md`** quando estiver pronto.