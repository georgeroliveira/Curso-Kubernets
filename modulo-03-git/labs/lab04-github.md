# Lab 4 - GitHub e Pull Request (60 minutos)

## Objetivo
Aprender o fluxo completo de colaboração com GitHub: criar fork, enviar alterações e abrir um Pull Request para o repositório da turma.

## O que vamos fazer
1. Criar conta e configurar GitHub (se necessário)
2. Fazer fork do repositório da turma
3. Clonar o fork localmente na VM
4. Criar branch e fazer alterações
5. Enviar branch para o GitHub
6. Abrir um Pull Request
7. Sincronizar repositório local com o remoto

---

## Parte 1: Preparação no GitHub (10 min)

### Passo 1.1 - Verificar conta no GitHub

**Acesse:** https://github.com

Se ainda não tem conta:
1. Clique em "Sign up"
2. Preencha dados (email, senha, username)
3. Verifique email
4. Complete setup inicial

---

### Passo 1.2 - Verificar SSH keys

**No terminal da VM:**

```bash
ssh -T git@github.com
```

**Saída esperada:**
```
Hi seu-usuario! You've successfully authenticated...
```

**Se falhar:**
- SSH keys não estão configuradas
- Volte ao Módulo 2 ou peça ajuda ao instrutor

---

### Passo 1.3 - Acessar repositório da turma

**O instrutor fornecerá o link, exemplo:**
```
https://github.com/devops-bootcamp/taskmanager-lab
```

**Abra no navegador.**

---

### Passo 1.4 - Fazer fork

1. Clique no botão **"Fork"** (canto superior direito)
2. Selecione sua conta como destino
3. Aguarde criação do fork
4. Você será redirecionado para seu fork

**URL do seu fork:**
```
https://github.com/seu-usuario/taskmanager-lab
```

**Checkpoint:** Seu fork existe e você está visualizando ele.

---

## Parte 2: Clonando e Configurando Localmente (10 min)

### Passo 2.1 - Voltar para pasta de trabalho

```bash
cd ~/devops-bootcamp
```

---

### Passo 2.2 - Clonar seu fork

**Copie a URL SSH do seu fork:**
- No GitHub, clique em **"Code"** > **"SSH"**
- Copie algo como: `git@github.com:seu-usuario/taskmanager-lab.git`

**Na VM:**
```bash
git clone git@github.com:seu-usuario/taskmanager-lab.git
```

**Saída esperada:**
```
Cloning into 'taskmanager-lab'...
remote: Enumerating objects: ...
Receiving objects: 100%
```

---

### Passo 2.3 - Entrar na pasta do fork

```bash
cd taskmanager-lab
```

---

### Passo 2.4 - Verificar repositório remoto

```bash
git remote -v
```

**Saída esperada:**
```
origin  git@github.com:seu-usuario/taskmanager-lab.git (fetch)
origin  git@github.com:seu-usuario/taskmanager-lab.git (push)
```

**Explicação:**
- **origin** - É seu fork no GitHub
- Você faz push/pull daqui

---

### Passo 2.5 - Adicionar repositório da turma como upstream

**URL do repo original fornecida pelo instrutor:**
```bash
git remote add upstream git@github.com:devops-bootcamp/taskmanager-lab.git
```

---

### Passo 2.6 - Verificar remotos configurados

```bash
git remote -v
```

**Agora você tem dois remotos:**
```
origin    git@github.com:seu-usuario/taskmanager-lab.git (fetch)
origin    git@github.com:seu-usuario/taskmanager-lab.git (push)
upstream  git@github.com:devops-bootcamp/taskmanager-lab.git (fetch)
upstream  git@github.com:devops-bootcamp/taskmanager-lab.git (push)
```

**Explicação:**
- **origin** - Seu fork (você pode escrever)
- **upstream** - Repo da turma (você só lê)

**Checkpoint:** Dois remotos configurados corretamente.

---

## Parte 3: Criando e Enviando Alterações (20 min)

### Passo 3.1 - Criar nova branch

```bash
git checkout -b feature/adiciona-contribuidor
```

**Saída:**
```
Switched to a new branch 'feature/adiciona-contribuidor'
```

---

### Passo 3.2 - Editar o README.md

**Abra o arquivo no VSCode:**
```bash
code README.md
```

**Navegue até o final do arquivo e adicione:**

```markdown

## Contribuidores

### Turma DevOps Bootcamp 2025

- Seu Nome Completo - GitHub: @seu-usuario
```

**Salve o arquivo** (`Ctrl + S`)

---

### Passo 3.3 - Verificar mudanças

```bash
git status
```

**Saída:**
```
On branch feature/adiciona-contribuidor
Changes not staged for commit:
        modified:   README.md
```

---

### Passo 3.4 - Ver diferenças

```bash
git diff README.md
```

**Você verá em verde** as linhas que adicionou.

---

### Passo 3.5 - Adicionar e commitar

```bash
git add README.md
git commit -m "adiciona Seu Nome na lista de contribuidores"
```

**Saída:**
```
[feature/adiciona-contribuidor abc123d] adiciona Seu Nome na lista de contribuidores
 1 file changed, 5 insertions(+)
```

---

### Passo 3.6 - Enviar branch para seu fork

```bash
git push origin feature/adiciona-contribuidor
```

**Saída:**
```
Enumerating objects: 5, done.
Counting objects: 100%
Writing objects: 100%
To github.com:seu-usuario/taskmanager-lab.git
 * [new branch]      feature/adiciona-contribuidor -> feature/adiciona-contribuidor
```

**Checkpoint:** Branch enviada com sucesso para o GitHub.

---

## Parte 4: Criando o Pull Request (15 min)

### Passo 4.1 - Abrir GitHub no navegador

Após o push, o GitHub mostra uma mensagem:

```
feature/adiciona-contribuidor had recent pushes
[Compare & pull request]
```

**Clique no botão verde** "Compare & pull request"

**Ou acesse manualmente:**
```
https://github.com/devops-bootcamp/taskmanager-lab/compare
```

---

### Passo 4.2 - Configurar o Pull Request

**Você verá:**
- **Base repository:** devops-bootcamp/taskmanager-lab (base: main)
- **Head repository:** seu-usuario/taskmanager-lab (compare: feature/adiciona-contribuidor)

**Preencha:**

**Título:**
```
Adiciona [Seu Nome] como contribuidor
```

**Descrição:**
```markdown
## Descrição
Adiciona meu nome na lista de contribuidores do projeto.

## Tipo de mudança
- [x] Documentação

## Checklist
- [x] Testei localmente
- [x] Segui convenções do projeto
- [x] Commit message está claro
```

---

### Passo 4.3 - Criar Pull Request

Clique em **"Create pull request"**

**Você será redirecionado** para a página do seu PR.

**URL exemplo:**
```
https://github.com/devops-bootcamp/taskmanager-lab/pull/123
```

**Checkpoint:** Pull Request criado com sucesso.

---

### Passo 4.4 - Revisar o Pull Request

**Na página do PR, você verá:**
- **Conversation:** Discussão e comentários
- **Commits:** Lista de commits incluídos
- **Files changed:** Diff das mudanças

**Clique em "Files changed"** para ver suas modificações.

---

### Passo 4.5 - Aguardar revisão

**O instrutor (ou colega) vai:**
1. Revisar suas mudanças
2. Adicionar comentários (se necessário)
3. Aprovar o PR
4. Fazer merge

**Status mudará para:**
- "Changes requested" (se precisa ajustar)
- "Approved" (se aprovado)
- "Merged" (após merge)

---

## Parte 5: Sincronizando com o Repositório Principal (5 min)

### Passo 5.1 - Aguardar merge

**Após o instrutor fazer merge**, seu PR mostrará:
```
Merged
seu-usuario merged 1 commit into devops-bootcamp:main
```

---

### Passo 5.2 - Voltar para branch main local

```bash
git checkout main
```

---

### Passo 5.3 - Baixar atualizações do upstream

```bash
git pull upstream main
```

**Saída:**
```
remote: Enumerating objects: ...
Unpacking objects: 100%
Updating abc123d..def456g
Fast-forward
 README.md | 5 +++++
 1 file changed, 5 insertions(+)
```

---

### Passo 5.4 - Enviar atualizações para seu fork

```bash
git push origin main
```

**Agora:**
- Repo da turma (upstream) - Atualizado
- Seu fork (origin) - Atualizado
- Seu local (VM) - Atualizado

Todos sincronizados.

---

### Passo 5.5 - Ver o resultado

**Acesse no navegador:**
```
https://github.com/devops-bootcamp/taskmanager-lab
```

**Seu nome deve aparecer** na lista de contribuidores do README.

**Checkpoint:** Ciclo completo de colaboração realizado com sucesso.

---

## Checkpoint Final

Ao final deste lab você deve ter:

- Conta GitHub configurada
- Fork criado com sucesso
- Branch criada e enviada para fork
- Pull Request aberto e mesclado (ou aguardando)
- Repositório local sincronizado com upstream
- Entendimento do fluxo fork -> branch -> PR

---

## Validação Completa

```bash
# 1. Verificar remotos configurados
git remote -v
# Deve mostrar origin e upstream

# 2. Verificar que está na main atualizada
git branch
git log --oneline -3

# 3. Verificar que seu nome está no README
cat README.md | grep "Seu Nome"

# 4. Ver histórico de branches
git log --oneline --graph --all
```

---

## Problemas Comuns

### "Permission denied (publickey)"

**Problema:** SSH keys não configuradas ou incorretas

**Solução:**
```bash
# Testar conexão
ssh -T git@github.com

# Se falhar, verificar chaves
ls -la ~/.ssh

# Ver chave pública para adicionar no GitHub
cat ~/.ssh/id_ed25519.pub
```

**No GitHub:**
- Settings > SSH and GPG keys > New SSH key
- Cole a chave e salve

---

### "fatal: remote origin already exists"

**Problema:** Tentou adicionar remote que já existe

**Solução:**
```bash
# Ver remotos existentes
git remote -v

# Remover e adicionar novamente
git remote remove origin
git remote add origin git@github.com:seu-usuario/repo.git
```

---

### "fatal: remote upstream already exists"

**Solução:**
```bash
# Atualizar URL do upstream
git remote set-url upstream git@github.com:devops-bootcamp/taskmanager-lab.git
```

---

### Pull Request não aparece

**Problema:** Branch não foi enviada corretamente

**Solução:**
```bash
# Verificar se branch existe no GitHub
git ls-remote origin

# Reenviar branch
git push origin feature/adiciona-contribuidor
```

---

### "Couldn't find remote ref"

**Problema:** Branch não existe no remoto

**Solução:**
```bash
# Verificar nome da branch local
git branch

# Enviar com nome correto
git push origin nome-da-branch-correta
```

---

### Conflito ao sincronizar

**Problema:** Mudanças conflitantes entre upstream e local

**Solução:**
```bash
# Fazer pull com rebase
git pull --rebase upstream main

# Se houver conflitos, resolver manualmente
# Abrir arquivos marcados com conflito
# Editar e remover marcadores <<< === >>>
git add arquivo-resolvido.md
git rebase --continue

# Enviar para fork
git push origin main
```

---

### Não consigo fazer push para upstream

**Problema:** Tentando enviar para repo que você não tem permissão

**Solução:**
- **Correto:** `git push origin main` (seu fork)
- **Errado:** `git push upstream main` (repo da turma)

Você só envia para **origin** (seu fork). O **upstream** é apenas para baixar atualizações.

---

## Conceitos Aprendidos

### Fork
- Cópia do repositório na sua conta GitHub
- Você tem permissão total de escrita
- Base para contribuir em projetos de terceiros
- Mantém link com repo original

### Origin vs Upstream
- **origin** - Seu fork (você escreve aqui)
- **upstream** - Repo original (você só lê)
- Sincronização: upstream -> local -> origin

### Pull Request (PR)
- Proposta de mudança para repo de terceiros
- Permite revisão antes do merge
- Espaço para discussão e feedback
- Padrão da indústria para colaboração

### Code Review
- Processo de revisar código de outros
- Identifica bugs, melhora qualidade
- Compartilha conhecimento na equipe
- Fundamental em times profissionais

---

## Fluxo Completo de Colaboração

```
1. Fork (GitHub)
   devops-bootcamp/repo -> seu-usuario/repo

2. Clone (VM)
   git clone git@github.com:seu-usuario/repo.git

3. Configurar upstream (VM)
   git remote add upstream git@github.com:devops-bootcamp/repo.git

4. Criar branch (VM)
   git checkout -b feature/minha-feature

5. Fazer mudanças e commitar (VM)
   git add .
   git commit -m "mensagem"

6. Enviar para fork (VM -> GitHub)
   git push origin feature/minha-feature

7. Abrir Pull Request (GitHub)
   De: seu-usuario/repo (feature/minha-feature)
   Para: devops-bootcamp/repo (main)

8. Code review (GitHub)
   Discussão, aprovação, merge

9. Sincronizar (GitHub -> VM)
   git checkout main
   git pull upstream main
   git push origin main
```

---

## Boas Práticas de Pull Request

### Título
```
# Bom
Adiciona endpoint /metrics para Prometheus
Corrige timeout no health check
Remove código duplicado no módulo auth

# Ruim
Update
Fix
Mudanças
PR123
```

### Descrição
```markdown
## Bom
Descrição clara do que foi feito
Por que foi feito
Como testar
Checklist de verificação

## Ruim
(vazio)
"mudanças"
"fix bug"
```

### Tamanho
- **Pequeno:** 1-50 linhas (ideal)
- **Médio:** 50-200 linhas (ok)
- **Grande:** 200+ linhas (dividir se possível)

### Commits
```bash
# Bom - histórico limpo
3 commits organizados
Mensagens descritivas

# Ruim - histórico poluído
20 commits tipo "fix", "teste", "ajuste"
```

---

## Comandos de Referência

```bash
# Configurar remotos
git remote add origin <url>
git remote add upstream <url>
git remote -v

# Trabalhar com fork
git clone <url-do-fork>
git checkout -b feature/nome
git push origin feature/nome

# Sincronizar
git pull upstream main
git push origin main

# Ver remotos
git remote show origin
git remote show upstream
```

---

## Diferença: Colaborador vs Contributor

### Colaborador (Collaborator)
- Tem permissão direta no repo
- Pode fazer push sem PR
- Geralmente time interno

### Contributor (via Fork)
- Sem permissão direta no repo
- Precisa fazer fork + PR
- Contribuidores externos
- **É o que você é neste lab**

---

## Próximos Passos

**Após este módulo, você domina:**
- Git local (commits, branches, merge)
- GitHub (fork, clone, push, pull)
- Pull Requests (criar, revisar, sincronizar)
- Colaboração em equipe

**No Módulo 4, você vai aprender:**
- Containerizar o TaskManager com Docker
- Criar Dockerfile otimizado
- Rodar aplicação em container isolado
- Preparar para orquestração

---

## Dicas Profissionais

### Antes de Abrir PR
1. Teste localmente
2. Revise suas próprias mudanças (Files changed)
3. Escreva descrição clara
4. Certifique-se que está na branch correta

### Durante Code Review
- Seja receptivo a feedback
- Pergunte se não entender comentário
- Faça ajustes solicitados rapidamente
- Agradeça revisores

### Depois do Merge
- Sincronize seu fork
- Delete branch local: `git branch -d nome`
- Delete branch remota: `git push origin --delete nome`

---

## Resumo do que Fizemos

1. Fizemos fork do repositório da turma
2. Clonamos fork localmente na VM
3. Configuramos remote upstream
4. Criamos branch de feature
5. Fizemos alterações e commitamos
6. Enviamos branch para GitHub
7. Abrimos Pull Request
8. Sincronizamos após merge

**Você agora sabe:**
- Colaborar em projetos de terceiros
- Usar fork + PR workflow
- Configurar múltiplos remotos
- Sincronizar repositórios
- Participar de code review

**Parabéns!** Você completou o Módulo 3 - Git do Zero ao Pull Request.

**Próximo módulo:** Docker Fundamentos - Containerizando o TaskManager.