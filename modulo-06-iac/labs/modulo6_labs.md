# Módulo 6 - Labs: Infrastructure as Code

## Lab 1: Scripts Shell para Automação (1h)

### Objetivo
Criar scripts Shell para automatizar instalação de dependências.

### Passos

#### 1.1 Script para instalar Docker
Criar `scripts/install-docker.sh`:
```bash
#!/bin/bash
set -e

echo "Instalando Docker e Docker Compose..."

# Atualizar sistema
sudo apt update

# Instalar dependências
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Adicionar chave GPG do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Adicionar repositório
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalação
docker --version
docker-compose --version

echo "Docker instalado com sucesso!"
echo "IMPORTANTE: Faça logout e login novamente para usar Docker sem sudo"
```

#### 1.2 Script para preparar ambiente
Criar `scripts/setup-environment.sh`:
```bash
#!/bin/bash
set -e

echo "Preparando ambiente para TaskManager..."

# Criar diretórios
mkdir -p ~/taskmanager-iac/{scripts,playbooks,inventory}
cd ~/taskmanager-iac

# Instalar dependências Python
sudo apt update
sudo apt install -y python3 python3-pip git

# Instalar Ansible
pip3 install ansible

# Verificar instalações
python3 --version
pip3 --version
ansible --version

# Criar arquivo de hosts para Ansible
cat > inventory/hosts <<EOF
[taskmanager]
localhost ansible_connection=local
EOF

echo "Ambiente preparado com sucesso!"
```

#### 1.3 Script para deploy do TaskManager
Criar `scripts/deploy-taskmanager.sh`:
```bash
#!/bin/bash
set -e

PROJECT_DIR="$HOME/taskmanager"
COMPOSE_FILE="docker-compose.yml"

echo "Fazendo deploy do TaskManager..."

# Verificar se Docker está rodando
if ! systemctl is-active --quiet docker; then
    echo "Iniciando Docker..."
    sudo systemctl start docker
fi

# Navegar para projeto
if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERRO: Diretório $PROJECT_DIR não encontrado"
    exit 1
fi

cd "$PROJECT_DIR"

# Verificar se docker-compose.yml existe
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "ERRO: Arquivo $COMPOSE_FILE não encontrado"
    exit 1
fi

# Parar containers existentes
echo "Parando containers existentes..."
docker-compose down || true

# Fazer pull das imagens
echo "Baixando imagens..."
docker-compose pull

# Fazer build da aplicação
echo "Construindo aplicação..."
docker-compose build

# Subir stack
echo "Subindo stack TaskManager..."
docker-compose up -d

# Aguardar aplicação ficar pronta
echo "Aguardando aplicação..."
sleep 30

# Verificar se está funcionando
if curl -f http://localhost/health >/dev/null 2>&1; then
    echo "TaskManager está funcionando!"
    echo "Acesse: http://localhost"
else
    echo "ERRO: TaskManager não respondeu"
    docker-compose logs
    exit 1
fi
```

#### 1.4 Tornar scripts executáveis
```bash
chmod +x scripts/*.sh
```

#### 1.5 Testar scripts
```bash
# Testar instalação do Docker (apenas se não tiver)
# ./scripts/install-docker.sh

# Preparar ambiente
./scripts/setup-environment.sh

# Testar deploy (se TaskManager já existir)
# ./scripts/deploy-taskmanager.sh
```

### Entregável
- Scripts Shell funcionais
- Instalação automatizada
- Deploy automatizado

---

## Lab 2: Ansible Básico (1h)

### Objetivo
Criar playbooks Ansible para automatizar configuração.

### Passos

#### 2.1 Instalar Ansible
```bash
# Se não instalou no Lab 1
pip3 install ansible
```

#### 2.2 Criar inventário
Criar `inventory/hosts`:
```ini
[taskmanager]
localhost ansible_connection=local

[taskmanager:vars]
ansible_python_interpreter=/usr/bin/python3
```

#### 2.3 Playbook para instalar Docker
Criar `playbooks/install-docker.yml`:
```yaml
---
- name: Instalar Docker no servidor
  hosts: taskmanager
  become: yes
  tasks:
    - name: Atualizar cache de pacotes
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Instalar dependências
      apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
          - gnupg
          - lsb-release
        state: present

    - name: Adicionar chave GPG do Docker
      apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Adicionar repositório Docker
      apt_repository:
        repo: "deb https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present

    - name: Instalar Docker
      apt:
        name:
          - docker-ce
          - docker-ce-cli
          - containerd.io
        state: present

    - name: Iniciar e habilitar Docker
      systemd:
        name: docker
        state: started
        enabled: yes

    - name: Adicionar usuário ao grupo docker
      user:
        name: "{{ ansible_user }}"
        groups: docker
        append: yes

    - name: Instalar Docker Compose
      get_url:
        url: "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-{{ ansible_system }}-{{ ansible_architecture }}"
        dest: /usr/local/bin/docker-compose
        mode: '0755'
      become: yes
```

#### 2.4 Playbook para preparar ambiente
Criar `playbooks/setup-environment.yml`:
```yaml
---
- name: Preparar ambiente TaskManager
  hosts: taskmanager
  become: yes
  tasks:
    - name: Instalar pacotes Python
      apt:
        name:
          - python3
          - python3-pip
          - git
          - curl
        state: present

    - name: Criar diretórios do projeto
      file:
        path: "{{ item }}"
        state: directory
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
      loop:
        - /home/{{ ansible_user }}/taskmanager
        - /home/{{ ansible_user }}/taskmanager/logs

    - name: Verificar se Git está configurado
      shell: git config --global user.name
      register: git_user
      failed_when: false
      become_user: "{{ ansible_user }}"

    - name: Configurar Git se necessário
      shell: |
        git config --global user.name "TaskManager Bot"
        git config --global user.email "bot@taskmanager.local"
      become_user: "{{ ansible_user }}"
      when: git_user.rc != 0
```

#### 2.5 Executar playbooks
```bash
# Instalar Docker
ansible-playbook -i inventory/hosts playbooks/install-docker.yml

# Preparar ambiente
ansible-playbook -i inventory/hosts playbooks/setup-environment.yml

# Verificar modo dry-run
ansible-playbook -i inventory/hosts playbooks/setup-environment.yml --check
```

### Entregável
- Playbooks Ansible funcionais
- Inventário configurado
- Automação idempotente

---

## Lab 3: Stack TaskManager Completa (1h)

### Objetivo
Criar playbook master para provisionar toda a stack.

### Passos

#### 3.1 Playbook principal
Criar `playbooks/site.yml`:
```yaml
---
- name: Provisionar Stack TaskManager Completa
  hosts: taskmanager
  become: yes
  vars:
    project_path: "/home/{{ ansible_user }}/taskmanager"
    taskmanager_repo: "https://github.com/SEU_USUARIO/taskmanager-devops.git"
  
  tasks:
    - name: Incluir instalação do Docker
      include: install-docker.yml

    - name: Incluir preparação do ambiente
      include: setup-environment.yml

    - name: Clonar repositório TaskManager
      git:
        repo: "{{ taskmanager_repo }}"
        dest: "{{ project_path }}"
        version: main
        force: yes
      become_user: "{{ ansible_user }}"

    - name: Criar docker-compose.yml
      copy:
        content: |
          version: '3.8'
          
          services:
            app:
              build: .
              ports:
                - "5000:5000"
              environment:
                - DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb
                - REDIS_URL=redis://redis:6379
                - FLASK_ENV=production
              depends_on:
                - db
                - redis
              volumes:
                - ./logs:/app/logs
          
            db:
              image: postgres:15
              environment:
                POSTGRES_DB: taskdb
                POSTGRES_USER: taskuser
                POSTGRES_PASSWORD: taskpass
              volumes:
                - postgres_data:/var/lib/postgresql/data
          
            redis:
              image: redis:7-alpine
              volumes:
                - redis_data:/data
              command: redis-server --appendonly yes
          
            nginx:
              image: nginx:alpine
              ports:
                - "80:80"
              volumes:
                - ./nginx.conf:/etc/nginx/conf.d/default.conf
              depends_on:
                - app
          
          volumes:
            postgres_data:
            redis_data:
        dest: "{{ project_path }}/docker-compose.yml"
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"

    - name: Criar configuração Nginx
      copy:
        content: |
          server {
              listen 80;
              server_name localhost;
          
              location / {
                  proxy_pass http://app:5000;
                  proxy_set_header Host $host;
                  proxy_set_header X-Real-IP $remote_addr;
                  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              }
          
              location /health {
                  access_log off;
                  return 200 "healthy from nginx\n";
              }
          }
        dest: "{{ project_path }}/nginx.conf"
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"

    - name: Parar containers existentes
      shell: docker-compose down
      args:
        chdir: "{{ project_path }}"
      become_user: "{{ ansible_user }}"
      ignore_errors: yes

    - name: Fazer build da aplicação
      shell: docker-compose build
      args:
        chdir: "{{ project_path }}"
      become_user: "{{ ansible_user }}"

    - name: Subir stack TaskManager
      shell: docker-compose up -d
      args:
        chdir: "{{ project_path }}"
      become_user: "{{ ansible_user }}"

    - name: Aguardar aplicação ficar pronta
      wait_for:
        host: localhost
        port: 80
        delay: 30
        timeout: 300

    - name: Verificar health check
      uri:
        url: http://localhost/health
        method: GET
      register: health_check
      retries: 5
      delay: 10
```

#### 3.2 Executar stack completa
```bash
# Executar playbook master
ansible-playbook -i inventory/hosts playbooks/site.yml

# Verificar se funcionou
curl http://localhost/health
```

#### 3.3 Criar playbook de limpeza
Criar `playbooks/cleanup.yml`:
```yaml
---
- name: Limpar ambiente TaskManager
  hosts: taskmanager
  become: yes
  tasks:
    - name: Parar todos os containers
      shell: docker-compose down -v
      args:
        chdir: "/home/{{ ansible_user }}/taskmanager"
      become_user: "{{ ansible_user }}"
      ignore_errors: yes

    - name: Remover containers não utilizados
      shell: docker system prune -f
      become_user: "{{ ansible_user }}"

    - name: Remover imagens não utilizadas
      shell: docker image prune -f
      become_user: "{{ ansible_user }}"
```

### Entregável
- Stack completa provisionada
- Playbook master funcionando
- TaskManager acessível via Nginx

---

## Lab 4: Pipeline GitHub Actions (30 min)

### Objetivo
Criar pipeline para validar configurações IaC.

### Passos

#### 4.1 Criar estrutura de validação
```bash
mkdir -p .github/workflows
```

#### 4.2 Pipeline de validação
Criar `.github/workflows/validate-iac.yml`:
```yaml
name: Validar Infrastructure as Code

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate-ansible:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout código
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Instalar dependências
      run: |
        pip install ansible ansible-lint yamllint

    - name: Validar sintaxe YAML
      run: |
        yamllint playbooks/ inventory/

    - name: Lint Ansible playbooks
      run: |
        ansible-lint playbooks/

    - name: Validar sintaxe Ansible
      run: |
        ansible-playbook --syntax-check playbooks/site.yml

  validate-docker:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout código
      uses: actions/checkout@v3

    - name: Validar docker-compose
      run: |
        # Simular docker-compose.yml se não existir
        if [ ! -f docker-compose.yml ]; then
          echo "Criando docker-compose.yml para validação..."
          cat > docker-compose.yml << EOF
          version: '3.8'
          services:
            app:
              build: .
              ports:
                - "5000:5000"
          EOF
        fi
        
        # Validar sintaxe
        docker-compose config

  validate-scripts:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout código
      uses: actions/checkout@v3

    - name: Validar scripts Shell
      run: |
        # Instalar shellcheck
        sudo apt-get update
        sudo apt-get install -y shellcheck
        
        # Validar todos os scripts .sh
        find scripts/ -name "*.sh" -exec shellcheck {} \;
```

#### 4.3 Configuração de validação
Criar `.yamllint.yml`:
```yaml
extends: default

rules:
  line-length:
    max: 120
  indentation:
    spaces: 2
  comments:
    min-spaces-from-content: 1
```

Criar `.ansible-lint`:
```yaml
skip_list:
  - yaml[line-length]
  - name[casing]
```

#### 4.4 README para IaC
Criar `README-IaC.md`:
```markdown
# TaskManager - Infrastructure as Code

## Como usar

### Provisionamento completo
```bash
# Clonar repositório
git clone https://github.com/SEU_USUARIO/taskmanager-iac.git
cd taskmanager-iac

# Executar provisionamento
ansible-playbook -i inventory/hosts playbooks/site.yml
```

### Scripts individuais
```bash
# Instalar Docker
./scripts/install-docker.sh

# Preparar ambiente
./scripts/setup-environment.sh

# Deploy TaskManager
./scripts/deploy-taskmanager.sh
```

### Validação local
```bash
# Validar YAML
yamllint playbooks/

# Validar Ansible
ansible-lint playbooks/
ansible-playbook --syntax-check playbooks/site.yml

# Validar scripts
shellcheck scripts/*.sh
```

## Estrutura
```
taskmanager-iac/
├── playbooks/          # Playbooks Ansible
├── inventory/          # Inventários
├── scripts/           # Scripts Shell
├── .github/workflows/ # Pipeline CI/CD
└── README-IaC.md     # Esta documentação
```
```

### Entregável
- Pipeline GitHub Actions funcionando
- Validação automática
- Repositório IaC completo

---

## Projeto Final

### Checklist de Validação

- [ ] Scripts Shell executam sem erro
- [ ] Playbooks Ansible são idempotentes
- [ ] Stack TaskManager provisionada automaticamente
- [ ] Pipeline GitHub Actions verde
- [ ] Documentação completa
- [ ] Repositório organizado

### Teste Final
```bash
# Teste completo - deve provisionar tudo do zero
ansible-playbook -i inventory/hosts playbooks/site.yml

# Verificar
curl http://localhost/health
curl http://localhost/api/tasks
```

Parabéns! Você automatizou completamente a infraestrutura do TaskManager!