# 🚀 Módulo 07 - CI/CD (Integração e Entrega Contínua)

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Ready-success)

## 📋 Visão Geral

Este módulo ensina os conceitos e práticas de CI/CD usando GitHub Actions, focando em pipelines multi-estágio, testes automatizados, segurança e deploy automatizado com Docker Compose.

## 🎯 Objetivos de Aprendizagem

Ao concluir este módulo, você será capaz de:

- ✅ Entender conceitos de CI/CD e pipelines
- ✅ Criar workflows no GitHub Actions
- ✅ Implementar pipeline multi-estágio (build → test → deploy)
- ✅ Automatizar deploy com Docker Compose
- ✅ Gerenciar secrets de forma segura
- ✅ Implementar estratégias de rollback

## 📚 Conteúdo Teórico

### 1. [Introdução ao CI/CD](teoria/01-introducao-cicd.md)
- O que é CI/CD
- Benefícios e práticas
- Pipeline as Code
- Ferramentas e comparações

### 2. [GitHub Actions](teoria/02-github-actions.md)
- Workflows, Jobs e Steps
- Events e Triggers
- Actions e Marketplace
- Matrix builds

### 3. [Pipeline Multi-estágio](teoria/03-pipeline-multiestagio.md)
- Build Stage
- Test Stage (Unit, Integration, E2E)
- Security Scanning
- Deploy Strategies

### 4. [Secrets e Rollback](teoria/04-secrets-rollback.md)
- Secrets Management
- Vault Integration
- Rollback Strategies
- Monitoring e Alertas

## 🔬 Laboratórios Práticos

### Lab 01: Primeiro Workflow
**Arquivo**: `labs/lab-01-primeiro-workflow/hello-world.yml`

Aprenda os conceitos básicos:
- Triggers (push, PR, manual)
- Jobs e dependências
- Variáveis e secrets
- Artifacts

```bash
# Como executar
1. Copie hello-world.yml para .github/workflows/
2. Faça commit e push
3. Vá em Actions no GitHub
4. Execute manualmente ou faça um push
```

### Lab 02: Pipeline Completo
**Arquivo**: `labs/lab-02-pipeline-completo/complete-pipeline.yml`

Pipeline profissional com:
- Build de imagem Docker
- Testes em paralelo
- Security scanning
- Deploy para staging/production
- Notificações

```bash
# Como executar
1. Configure os secrets no GitHub
2. Crie ambientes (staging/production)
3. Push para develop → staging
4. Tag com v*.*.* → production
```

### Lab 03: Deploy com Docker Compose
**Arquivo**: `labs/lab-03-deploy-compose/deploy-compose.yml`

Stack completa com:
- PostgreSQL + Redis
- Load balancer com Nginx
- 3 instâncias da aplicação
- Health checks
- Rolling updates

```bash
# Como executar
1. Configure docker-compose.yml
2. Push alterações
3. Pipeline fará build, test e deploy
4. Acesse http://localhost
```

## 📁 Estrutura do Módulo

```
modulo-07-cicd/
├── .github/
│   └── workflows/           # Workflows de exemplo
│       ├── ci.yml           # Integração contínua
│       ├── cd.yml           # Deploy contínuo
│       └── security.yml     # Security scanning
├── teoria/
│   ├── 01-introducao-cicd.md
│   ├── 02-github-actions.md
│   ├── 03-pipeline-multiestagio.md
│   └── 04-secrets-rollback.md
├── labs/
│   ├── lab-01-primeiro-workflow/
│   │   └── hello-world.yml
│   ├── lab-02-pipeline-completo/
│   │   └── complete-pipeline.yml
│   └── lab-03-deploy-compose/
│       └── deploy-compose.yml
├── scripts/
│   ├── deploy.sh            # Script de deploy
│   ├── rollback.sh          # Script de rollback
│   └── health-check.sh      # Health checks
├── docker-compose.yml        # Stack da aplicação
├── Dockerfile               # Imagem da aplicação
└── README.md                # Este arquivo
```

## 🛠️ Configuração Inicial

### 1. Pré-requisitos

- Conta no GitHub
- Docker instalado localmente
- Git configurado
- Node.js 16+ (opcional)

### 2. Fork e Clone

```bash
# Fork este repositório no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/modulo-07-cicd.git
cd modulo-07-cicd

# Configure upstream
git remote add upstream https://github.com/original/modulo-07-cicd.git
```

### 3. Configurar Secrets no GitHub

```bash
# No GitHub: Settings → Secrets and variables → Actions

# Secrets necessários:
DOCKER_USERNAME       # DockerHub username
DOCKER_PASSWORD       # DockerHub password
SLACK_WEBHOOK        # URL do webhook do Slack
SSH_PRIVATE_KEY      # Chave SSH para deploy
HOST_SERVER          # IP ou hostname do servidor
```

### 4. Criar Environments

```bash
# No GitHub: Settings → Environments

# Staging
- Nome: staging
- URL: https://staging.exemplo.com
- Sem aprovação

# Production
- Nome: production  
- URL: https://app.exemplo.com
- Requer aprovação
- Reviewers: você
```

## 🚀 Executando os Laboratórios

### Quick Start

```bash
# Lab 01 - Primeiro Workflow
cp labs/lab-01-primeiro-workflow/hello-world.yml .github/workflows/
git add . && git commit -m "Add first workflow"
git push origin main

# Lab 02 - Pipeline Completo
cp labs/lab-02-pipeline-completo/complete-pipeline.yml .github/workflows/
# Configure secrets primeiro!
git add . && git commit -m "Add complete pipeline"
git push origin develop

# Lab 03 - Deploy com Compose
cp labs/lab-03-deploy-compose/deploy-compose.yml .github/workflows/
docker-compose up -d  # Teste local primeiro
git add . && git commit -m "Add compose deployment"
git push origin main
```

## 📊 Workflows Disponíveis

### 1. CI - Continuous Integration
```yaml
on: [push, pull_request]
jobs:
  - lint
  - test
  - build
  - security-scan
```

### 2. CD - Continuous Deployment
```yaml
on:
  push:
    branches: [main]
    tags: ['v*']
jobs:
  - deploy-staging
  - deploy-production
```

### 3. Nightly Builds
```yaml
on:
  schedule:
    - cron: '0 2 * * *'
jobs:
  - full-test-suite
  - performance-tests
  - security-audit
```

## 🔧 Comandos Úteis

### GitHub CLI

```bash
# Listar workflows
gh workflow list

# Ver runs
gh run list

# Executar workflow manualmente
gh workflow run hello-world.yml

# Ver logs
gh run view <run-id> --log

# Cancelar run
gh run cancel <run-id>
```

### Docker Commands

```bash
# Build local
docker build -t myapp .

# Run tests
docker run --rm myapp npm test

# Docker Compose
docker-compose up -d
docker-compose ps
docker-compose logs -f
docker-compose down
```

### Debugging Workflows

```bash
# Habilitar debug no GitHub Actions
# Adicione estes secrets:
ACTIONS_RUNNER_DEBUG: true
ACTIONS_STEP_DEBUG: true

# Ou use tmate para debug interativo:
- uses: mxschmitt/action-tmate@v3
  if: ${{ github.event_name == 'workflow_dispatch' }}
```

## 📈 Métricas e Monitoramento

### Métricas do Pipeline

| Métrica | Meta | Como Medir |
|---------|------|------------|
| Build Success Rate | > 95% | Successful builds / Total builds |
| Deploy Frequency | Daily | Deployments per day |
| Lead Time | < 1 hour | Commit to production time |
| MTTR | < 30 min | Time to recover from failure |
| Test Coverage | > 80% | Lines covered / Total lines |

### Dashboard de Monitoramento

```yaml
# Exemplo de métricas para coletar
metrics:
  - pipeline_duration_seconds
  - build_success_total
  - deploy_success_total
  - rollback_count_total
  - test_execution_time_seconds
```

## 🔐 Segurança

### Checklist de Segurança

- [ ] Secrets nunca no código
- [ ] Use GitHub Secrets
- [ ] Rotacione secrets regularmente
- [ ] Pin versions das Actions
- [ ] Security scanning (Trivy, Snyk)
- [ ] SAST/DAST scanning
- [ ] Dependency updates (Dependabot)
- [ ] Code signing
- [ ] Audit logs

### Exemplo de Security Workflow

```yaml
- name: Security Scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    scan-ref: '.'
    severity: 'CRITICAL,HIGH'
```

## 🔄 Estratégias de Deploy

### 1. Blue-Green

```
[Blue - Produção Atual] ← Tráfego
[Green - Nova Versão] ← Deploy
[Green] ← Testes
[Green] ← Switch Tráfego
[Blue] ← Standby/Remove
```

### 2. Canary

```
95% → Versão Estável
5% → Nova Versão
Monitor → Increase %
100% → Nova Versão
```

### 3. Rolling Update

```
Instance 1 → Update → Healthy → Continue
Instance 2 → Update → Healthy → Continue
Instance 3 → Update → Healthy → Done
```

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. "Permission denied" no workflow
```yaml
# Solução: Adicione permissões
permissions:
  contents: read
  packages: write
```

#### 2. Secrets não funcionam
```yaml
# Verifique:
- Nome do secret está correto
- Secret existe no ambiente certo
- Não use secrets em PRs de forks
```

#### 3. Docker build falha
```yaml
# Use buildx para multi-platform
- uses: docker/setup-buildx-action@v2
```

#### 4. Timeout em jobs
```yaml
# Configure timeout
jobs:
  test:
    timeout-minutes: 30
```

## 📚 Recursos Adicionais

### Documentação Oficial
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

### Tutoriais e Guias
- [GitHub Actions Tutorial](https://github.com/skills/hello-github-actions)
- [Docker with GitHub Actions](https://docs.docker.com/ci-cd/github-actions/)
- [Security Best Practices](https://docs.github.com/en/actions/security-guides)

### Ferramentas Úteis
- [act](https://github.com/nektos/act) - Run GitHub Actions locally
- [actionlint](https://github.com/rhysd/actionlint) - Static checker
- [GitHub CLI](https://cli.github.com/) - Command line interface

## ✅ Checklist de Conclusão

Ao finalizar o módulo, você deve ser capaz de:

- [ ] Criar workflows do zero
- [ ] Implementar pipeline multi-estágio
- [ ] Configurar matrix builds
- [ ] Gerenciar secrets com segurança
- [ ] Fazer deploy automatizado
- [ ] Implementar rollback automático
- [ ] Configurar notificações
- [ ] Monitorar pipelines
- [ ] Debugar workflows
- [ ] Otimizar performance

## 🎯 Projeto Final

### Requisitos

Crie um pipeline completo que:

1. **Build**
   - Crie imagem Docker multi-stage
   - Push para registry
   - Gere SBOM

2. **Test**
   - Unit tests com coverage
   - Integration tests
   - E2E tests
   - Performance tests

3. **Security**
   - Vulnerability scanning
   - Secret scanning
   - SAST analysis

4. **Deploy**
   - Deploy staging automático
   - Deploy production com aprovação
   - Health checks
   - Rollback automático

5. **Monitor**
   - Métricas de pipeline
   - Alertas de falha
   - Dashboard de status

### Entrega

```bash
# Estrutura esperada
seu-projeto/
├── .github/workflows/
│   ├── ci.yml
│   ├── cd.yml
│   └── security.yml
├── docker-compose.yml
├── Dockerfile
├── tests/
├── scripts/
└── README.md

# Critérios de avaliação
- Pipeline funcional: 40%
- Testes automatizados: 20%
- Security scanning: 20%
- Documentação: 10%
- Boas práticas: 10%
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma feature branch (`git checkout -b feature/amazing`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing`)
5. Abra um Pull Request

## 📝 Licença

Este material é distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 👨‍🏫 Suporte

- 📧 Email: suporte@exemplo.com
- 💬 Discord: [Link para servidor](https://discord.gg/exemplo)
- 🐙 GitHub Issues: [Abrir issue](https://github.com/seu-usuario/modulo-07-cicd/issues)

## 🏆 Certificado

Ao completar todos os laboratórios e o projeto final, você receberá:
- Certificado de conclusão
- Badge "CI/CD Expert"
- Acesso ao próximo módulo

---

**🚀 Parabéns por chegar até aqui!**

Você agora domina CI/CD com GitHub Actions. Continue praticando e construindo pipelines cada vez mais robustos!

💡 **Próximo módulo**: Kubernetes e Orquestração Avançada