# Conceitos Fundamentais de Infrastructure as Code

## O que é Infrastructure as Code?

Infrastructure as Code (IaC) é a prática de gerenciar e provisionar infraestrutura através de código, em vez de processos manuais.

### Definição Prática
- **Código**: Scripts, playbooks, templates
- **Infraestrutura**: Servidores, redes, aplicações, configurações
- **Automação**: Deploy, configuração, manutenção

### Exemplo TaskManager
```bash
# Manual (Módulo 5)
ssh servidor
sudo apt install docker
sudo docker-compose up

# IaC (Módulo 6)  
ansible-playbook deploy-taskmanager.yml
```

---

## Problemas da Configuração Manual

### 1. Snowflake Servers
Cada servidor único como floco de neve:
- Configurações diferentes
- Patches aplicados em momentos diferentes
- Histórico desconhecido
- Impossível replicar

### 2. Drift de Configuração
```bash
# Servidor A
Versão Docker: 20.10.5
PostgreSQL: 13.2

# Servidor B  
Versão Docker: 20.10.8
PostgreSQL: 13.7

# Comportamentos diferentes!
```

### 3. Falta de Rastreabilidade
- "Quem mudou o nginx?"
- "Quando foi alterado?"
- "Como voltar a versão anterior?"

### 4. Dificuldade de Escala
- 1 servidor: 10 comandos
- 10 servidores: 100 comandos
- 100 servidores: 1000 comandos

---

## Benefícios do IaC

### 1. Versionamento
```bash
git log --oneline
a1b2c3d Adiciona Redis ao TaskManager
d4e5f6g Atualiza versão PostgreSQL
g7h8i9j Configura Nginx load balancer
```

### 2. Reprodutibilidade
```yaml
# Mesmo código = mesmo resultado
- name: Instalar Docker
  version: 20.10.21
  state: present
```

### 3. Idempotência
```bash
# Executar N vezes = mesmo resultado
ansible-playbook site.yml  # 1ª vez: instala tudo
ansible-playbook site.yml  # 2ª vez: "nada a fazer"
```

### 4. Documentação Viva
```yaml
# O código É a documentação
- name: Configurar TaskManager
  vars:
    flask_port: 5000
    postgres_version: 15
    redis_enabled: true
```

### 5. Rollback Rápido
```bash
git revert a1b2c3d
ansible-playbook site.yml  # Volta configuração anterior
```

---

## Princípios Fundamentais

### 1. Idempotência

**Definição**: Executar N vezes produz o mesmo resultado.

```bash
# NÃO idempotente
echo "nova linha" >> arquivo.txt

# Idempotente  
echo "conteúdo fixo" > arquivo.txt
```

**No TaskManager**:
```yaml
- name: Criar diretório logs
  file:
    path: /app/logs
    state: directory  # Cria se não existe, ignora se existe
```

### 2. Declarativo vs Imperativo

**Imperativo** (como fazer):
```bash
apt update
apt install docker
systemctl start docker
systemctl enable docker
```

**Declarativo** (o que quero):
```yaml
- name: Docker instalado e rodando
  package:
    name: docker
    state: present
  service:
    name: docker
    state: started
    enabled: yes
```

### 3. Imutabilidade

**Filosofia**: Não modificar, substituir.

```bash
# Mutável (ruim)
ssh servidor
apt upgrade docker

# Imutável (bom)
ansible-playbook update-docker.yml  # Substitui configuração completa
```

---

## Ferramentas IaC

### Categorias

**Gerenciamento de Configuração**:
- Ansible (usado no curso)
- Chef
- Puppet
- SaltStack

**Provisionamento de Infraestrutura**:
- Terraform
- CloudFormation (AWS)
- ARM Templates (Azure)

**Orquestração de Containers**:
- Docker Compose (Módulo 5)
- Kubernetes (futuro)
- Docker Swarm

### Por que Ansible?

**Vantagens**:
- Agentless (SSH apenas)
- YAML simples
- Idempotente por padrão
- Grande comunidade
- Módulos para tudo

**Exemplo TaskManager**:
```yaml
- name: Deploy TaskManager Stack
  docker_compose:
    project_src: /app/taskmanager
    state: present
```

---

## Padrões de IaC

### 1. Estrutura de Repositório
```
taskmanager-iac/
├── playbooks/          # Ansible playbooks
├── inventory/          # Servers/grupos
├── group_vars/         # Variáveis por grupo
├── host_vars/          # Variáveis por servidor
├── roles/              # Roles reutilizáveis
└── scripts/            # Scripts auxiliares
```

### 2. Ambientes Separados
```
inventory/
├── development/
├── staging/
└── production/
```

### 3. Secrets Management
```yaml
# Não fazer
database_password: "senha123"

# Fazer
database_password: "{{ vault_database_password }}"
```

### 4. Testing
```bash
# Dry run
ansible-playbook site.yml --check

# Lint
ansible-lint playbooks/

# Syntax check
ansible-playbook --syntax-check site.yml
```

---

## IaC no Contexto TaskManager

### Evolução dos Módulos

**Módulo 1-2**: Manual total
- Comandos individuais
- Configuração ad-hoc

**Módulo 3**: Versionamento de código
- Git para aplicação
- Infraestrutura ainda manual

**Módulo 4**: Containerização
- Docker para portabilidade
- Dockerfile = IaC básico

**Módulo 5**: Orquestração
- docker-compose.yml = IaC containers
- Multi-container automatizado

**Módulo 6**: IaC completo
- Ansible para tudo
- Zero configuração manual

### Exemplo Prático
```yaml
# ansible-playbook taskmanager.yml executa:
1. Atualiza sistema
2. Instala Docker + Compose  
3. Clona código TaskManager
4. Configura PostgreSQL
5. Configura Redis
6. Configura Nginx
7. Sobe stack completa
8. Verifica health checks
```

---

## Boas Práticas

### 1. Keep It Simple
```yaml
# Bom
- name: Instalar pacotes
  apt:
    name: "{{ packages }}"

# Ruim (complexo demais)
- name: Verificar se existe, baixar, compilar, instalar...
```

### 2. Use Roles
```yaml
# taskmanager.yml
- hosts: all
  roles:
    - common
    - docker
    - taskmanager
```

### 3. Versionamento Semântico
```bash
git tag v1.0.0  # TaskManager básico
git tag v1.1.0  # Adiciona Redis
git tag v2.0.0  # Mudança breaking
```

### 4. Documentation as Code
```yaml
- name: Configure Nginx for TaskManager load balancing
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  # Autodocumentado no próprio código
```

### 5. Fail Fast
```yaml
- name: Verificar pré-requisitos
  assert:
    that:
      - ansible_version.full is version('2.9', '>=')
      - ansible_os_family == "Debian"
```

---

## Próximos Passos

### Módulo 6 Labs
1. **Shell Scripts**: Automação básica
2. **Ansible**: Playbooks TaskManager
3. **Pipeline**: Validação automática

### Além do Módulo 6
- **Terraform**: Infraestrutura cloud
- **Kubernetes**: Orquestração avançada
- **GitOps**: Deploy via Git

---

## Recursos Adicionais

- [Ansible Documentation](https://docs.ansible.com/)
- [Infrastructure as Code Patterns](https://infrastructure-as-code.com/)
- [12 Factor App](https://12factor.net/)
- [DevOps Handbook](https://itrevolution.com/the-devops-handbook/)