# Módulo 06 - Infrastructure as Code (IaC)

## O que você vai aprender

Em 4 horas, você vai conquistar:
- Automatizar provisionamento da stack TaskManager
- Criar scripts Shell para instalação de pacotes
- Desenvolver playbooks Ansible idempotentes
- Versionar infraestrutura no Git
- Validar configurações com GitHub Actions

## Pré-requisitos

Antes da aula, você precisa:
- [ ] TaskManager multi-container funcionando (Módulo 5)
- [ ] VM Ubuntu configurada
- [ ] Git e GitHub configurados
- [ ] Conhecimento básico de terminal Linux

## Como estudar este módulo

1. **Conceitos (30 min):** Entender IaC e idempotência
2. **Shell Scripts (1h):** Automatizar instalações
3. **Ansible (2h):** Playbooks para stack completa
4. **Validação (30 min):** Pipeline no GitHub Actions

## Estrutura do Módulo

```
modulo-06-iac/
├── README.md              → Você está aqui
├── labs/
│   └── labs.md           → Exercícios práticos (foco principal)
└── teoria/
    ├── conceitos-iac.md   → Fundamentos de IaC
    ├── shell-scripts.md   → Automação com Bash
    ├── ansible-basico.md  → Playbooks e inventários
    └── pipeline-cicd.md   → Validação automatizada
```

## Cronograma de 4 horas

| Tempo | Atividade | Objetivo |
|-------|-----------|----------|
| 0:00-0:30 | Conceitos | Entender IaC e benefícios |
| 0:30-1:30 | Lab 1 | Scripts Shell para Docker |
| 1:30-2:30 | Lab 2 | Ansible para TaskManager |
| 2:30-3:30 | Lab 3 | Playbook da stack completa |
| 3:30-4:00 | Lab 4 | Pipeline GitHub Actions |

## Evolução do TaskManager

**Módulo 5 (anterior):**
- Stack multi-container (Flask + PostgreSQL + Redis + Nginx)
- docker-compose.yml manual
- Configuração manual da VM

**Módulo 6 (atual):**
- Provisionamento automatizado
- Scripts Shell para dependências
- Playbooks Ansible para stack
- Pipeline de validação

**Módulo 7 (próximo):**
- CI/CD completo
- Deploy automatizado
- Testes automatizados

## Checklist de Conclusão

Ao final do módulo você deve ter:
- [ ] Scripts Shell para instalar Docker/Compose
- [ ] Playbook Ansible para provisionar VM
- [ ] Repositório IaC versionado
- [ ] Pipeline GitHub Actions funcionando
- [ ] Stack TaskManager provisionada automaticamente

## Automação Final

```
┌─────────────────────────────────────┐
│           GitHub Actions            │
│        (Validação + Deploy)         │
└─────────────────────────────────────┘
                    │
┌─────────────────────────────────────┐
│           Ansible Playbook          │
│      (Provisiona tudo na VM)        │
└─────────────────────────────────────┘
                    │
            ┌───────┬───────┐
            │       │       │
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Script 1:   │ │ Script 2:   │ │ Script 3:   │
│ Dependências│ │ Docker +    │ │ TaskManager │
│ (Python/Git)│ │ Compose     │ │ Deploy      │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Comandos que você vai dominar

```bash
# Shell Scripts
./install-docker.sh
./setup-environment.sh

# Ansible
ansible-playbook -i inventory site.yml
ansible-playbook site.yml --check
ansible-vault encrypt secrets.yml

# Validação
ansible-lint playbook.yml
yamllint docker-compose.yml
```

## Resultado Final

Após este módulo você terá:
1. Infraestrutura 100% automatizada
2. Zero configuração manual
3. Ambientes reproduzíveis
4. Pipeline de validação
5. Repositório IaC profissional

Um comando provisionará toda a stack TaskManager do zero!

---

**Próximo módulo:** CI/CD Pipeline - Deploy Automatizado