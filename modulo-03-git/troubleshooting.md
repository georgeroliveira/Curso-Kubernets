# Troubleshooting - Módulo 03: Git

Guia rápido de soluções para os 10 problemas mais comuns.

---

## 1. Permission denied ao fazer git push

**Você vê:**
```
Permission denied (publickey).
fatal: Could not read from remote repository.
```

**Solução:**
```bash
# Testar conexão GitHub
ssh -T git@github.com

# Se der erro, verificar se chave existe
ls -la ~/.ssh/

# Se não existir id_ed25519, criar chave SSH
ssh-keygen -t ed25519 -C "seu.email@exemplo.com"
# Pressione Enter 3 vezes (sem senha)

# Copiar chave pública
cat ~/.ssh/id_ed25519.pub

# Adicionar no GitHub:
# 1. Acesse: https://github.com/settings/keys
# 2. Clique "New SSH key"
# 3. Cole TODO o conteúdo da chave
# 4. Clique "Add SSH key"

# Testar novamente
ssh -T git@github.com
```

**Deve aparecer:** `Hi seu-usuario! You've successfully authenticated...`

---

## 2. VSCode Remote SSH não conecta na VM

**Você vê:**
- "Could not resolve hostname"
- "Connection timeout"
- "Connection refused"

**Solução:**
```bash
# Na VM Ubuntu (via console direto), verificar IP
hostname -I

# Anotar o IP (exemplo: 192.168.64.5)

# No VSCode (seu computador):
# Ctrl + Shift + P
# Remote-SSH: Connect to Host
# Digite: devops@<ip-anotado>

# Se continuar com erro, verificar SSH rodando (na VM)
sudo systemctl status ssh
sudo systemctl start ssh
sudo systemctl enable ssh

# Verificar firewall (na VM)
sudo ufw allow 22/tcp
sudo ufw status
```

---

## 3. Git não instalado

**Você vê:**
```
git: command not found
```

**Solução:**
```bash
# Instalar Git
sudo apt update
sudo apt install git -y

# Verificar instalação
git --version
```

---

## 4. ModuleNotFoundError no Python

**Você vê:**
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'dotenv'
```

**Solução:**
```bash
# Verificar se está no diretório correto
pwd
# Deve mostrar: /home/devops/devops-bootcamp/taskmanager-starter

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se ativou (deve aparecer (venv) no prompt)
# Se ambiente virtual não existe, criar
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

---

## 5. Ambiente virtual não ativa

**Você vê:**
- Comando `source venv/bin/activate` não funciona
- Prompt não mostra `(venv)`

**Solução:**
```bash
# Remover ambiente virtual corrompido
rm -rf venv

# Recriar ambiente virtual
python3 -m venv venv

# Ativar
source venv/bin/activate

# Verificar ativação
which python
# Deve mostrar: /home/devops/devops-bootcamp/taskmanager-starter/venv/bin/python

# Reinstalar dependências
pip install -r requirements.txt
```

---

## 6. Porta 5000 já em uso

**Você vê:**
```
OSError: [Errno 98] Address already in use
```

**Solução:**
```bash
# Verificar processo usando porta 5000
sudo lsof -i :5000

# Matar processo
kill -9 <PID>

# Ou mudar porta da aplicação
# Editar .env
echo "PORT=5001" >> .env

# Rodar na nova porta
python app.py
```

---

## 7. Git config não configurado

**Você vê:**
```
*** Please tell me who you are.
Run: git config --global user.email "you@example.com"
```

**Solução:**
```bash
# Configurar nome e email
git config --global user.name "Seu Nome Completo"
git config --global user.email "seu.email@exemplo.com"

# IMPORTANTE: Use o mesmo email do GitHub
# Verificar: https://github.com/settings/emails

# Verificar configuração
git config --list
```

---

## 8. Arquivo .env não carrega

**Você vê:**
- Variáveis de ambiente não funcionam
- App usa valores padrão em vez dos definidos

**Solução:**
```bash
# Verificar se arquivo .env existe
ls -la .env

# Se não existe, criar a partir do exemplo
cp .env.example .env

# Verificar se python-dotenv está instalado
pip list | grep dotenv

# Se não estiver, instalar
pip install python-dotenv

# Verificar se app.py carrega .env
# Deve ter estas linhas no início:
# from dotenv import load_dotenv
# load_dotenv()

# Testar carregamento
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('PORT', 'não carregou'))"
```

---

## 9. Merge dá conflito

**Você vê:**
```
CONFLICT (content): Merge conflict in app.py
Automatic merge failed; fix conflicts and then commit the result.
```

**Solução:**
```bash
# Ver arquivos com conflito
git status

# Abrir arquivo no VSCode
# Procurar por marcadores:
# <<<<<<< HEAD
# código da branch atual
# =======
# código da branch sendo mesclada
# >>>>>>> nome-da-branch

# Editar arquivo:
# 1. Escolher qual versão manter (ou combinar)
# 2. Remover marcadores <<<, ===, >>>
# 3. Salvar arquivo

# Adicionar arquivo resolvido
git add app.py

# Completar merge
git commit -m "resolve conflito de merge"

# Verificar
git status
```

---

## 10. Git mostra arquivo .env como modificado

**Você vê:**
```
Changes not staged for commit:
  modified:   .env
```

**Mas .env deveria ser ignorado**

**Solução:**
```bash
# Verificar se .gitignore existe e contém .env
cat .gitignore | grep .env

# Se não tiver, adicionar
echo ".env" >> .gitignore

# Se .env já foi commitado antes, remover do Git
git rm --cached .env

# Commitar remoção
git commit -m "remove .env do versionamento"

# Verificar
git status
# .env não deve mais aparecer
```

---

## Quando chamar o instrutor

Chame o instrutor se:
- Problema não está nesta lista
- Seguiu solução mas erro continua
- Mensagem de erro é diferente das mostradas
- Resolveu mas quer entender o porquê

---

## Comandos úteis para diagnóstico
```bash
# Verificar versões
git --version
python3 --version
pip --version

# Verificar localização
pwd
which python
which git

# Verificar status
git status
git log --oneline -5

# Verificar configuração
git config --list
git remote -v

# Verificar ambiente Python
pip list
which python

# Verificar processos/portas
ps aux | grep python
sudo lsof -i :5000
```

---

Versão: 1.0 - Módulo 03 Git
Atualizado: 2025