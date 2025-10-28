# GitHub Actions - Automação Nativa do GitHub

## O que é GitHub Actions?

GitHub Actions é uma plataforma de CI/CD integrada ao GitHub que permite automatizar workflows diretamente do repositório.

## Conceitos Fundamentais

### 1. Workflow
Processo automatizado configurável (arquivo YAML)
```yaml
# .github/workflows/meu-workflow.yml
name: Meu Workflow
on: push
jobs:
  meu-job:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello World"
```

### 2. Events (Gatilhos)
O que dispara o workflow
```yaml
# Push em qualquer branch
on: push

# Push em branches específicas
on:
  push:
    branches: [main, develop]

# Pull request
on: pull_request

# Schedule (cron)
on:
  schedule:
    - cron: '0 2 * * *'  # 2AM diariamente

# Manual
on: workflow_dispatch

# Múltiplos eventos
on: [push, pull_request]
```

### 3. Jobs
Conjunto de steps que rodam no mesmo runner
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm build
  
  test:
    needs: build  # Depende do job build
    runs-on: ubuntu-latest
    steps:
      - run: npm test
```

### 4. Steps
Tarefas individuais em um job
```yaml
steps:
  # Action
  - uses: actions/checkout@v3
  
  # Run command
  - run: echo "Hello"
  
  # Step com nome
  - name: Install dependencies
    run: npm install
  
  # Multi-line command
  - run: |
      echo "Line 1"
      echo "Line 2"
```

### 5. Actions
Comandos reutilizáveis
```yaml
# Actions oficiais
- uses: actions/checkout@v3
- uses: actions/setup-node@v3
  with:
    node-version: '16'

# Actions do marketplace
- uses: docker/setup-buildx-action@v2
- uses: docker/login-action@v2
```

### 6. Runners
Máquinas que executam os jobs
```yaml
# GitHub-hosted runners
runs-on: ubuntu-latest
runs-on: windows-latest
runs-on: macos-latest

# Self-hosted runner
runs-on: self-hosted
```

## Sintaxe Detalhada

### Variáveis e Contextos
```yaml
env:
  # Variável global
  GLOBAL_VAR: valor

jobs:
  build:
    env:
      # Variável do job
      JOB_VAR: valor
    
    steps:
      - env:
          # Variável do step
          STEP_VAR: valor
        run: |
          echo $GLOBAL_VAR
          echo $JOB_VAR
          echo $STEP_VAR
          echo ${{ github.repository }}
          echo ${{ github.ref }}
          echo ${{ github.sha }}
```

### Condicionais
```yaml
steps:
  - name: Run only on main
    if: github.ref == 'refs/heads/main'
    run: echo "Deploy to production"
  
  - name: Run on PR
    if: github.event_name == 'pull_request'
    run: echo "Run extra tests"
  
  - name: Always run
    if: always()
    run: echo "Cleanup"
  
  - name: Run on failure
    if: failure()
    run: echo "Something failed"
```

### Matrix Strategy
```yaml
strategy:
  matrix:
    node: [14, 16, 18]
    os: [ubuntu-latest, windows-latest]
    
runs-on: ${{ matrix.os }}
steps:
  - uses: actions/setup-node@v3
    with:
      node-version: ${{ matrix.node }}
  - run: npm test
```

### Outputs
```yaml
jobs:
  job1:
    outputs:
      version: ${{ steps.get_version.outputs.version }}
    steps:
      - id: get_version
        run: echo "version=1.0.0" >> $GITHUB_OUTPUT
  
  job2:
    needs: job1
    steps:
      - run: echo "Version is ${{ needs.job1.outputs.version }}"
```

## Workflows Práticos

### 1. CI Básico para Node.js
```yaml
name: Node.js CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [14, 16, 18]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
```

### 2. Docker Build e Push
```yaml
name: Docker CI/CD

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 3. Deploy com Docker Compose
```yaml
name: Deploy to Server

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Copy files to server
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          source: "docker-compose.yml,nginx.conf"
          target: "/app"
      
      - name: Deploy with Docker Compose
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /app
            docker-compose pull
            docker-compose up -d
            docker-compose ps
```

## Secrets e Variáveis

### Configurar Secrets
```bash
# No GitHub:
Settings → Secrets and variables → Actions → New repository secret

# Tipos de secrets:
- Repository secrets (específico do repo)
- Organization secrets (todos os repos da org)
- Environment secrets (por ambiente)
```

### Usar Secrets
```yaml
steps:
  - name: Login to DockerHub
    env:
      DOCKER_USER: ${{ secrets.DOCKER_USER }}
      DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
    run: |
      echo $DOCKER_PASSWORD | docker login -u $DOCKER_USER --password-stdin
```

### Variáveis de Ambiente
```yaml
env:
  # Nível workflow
  NODE_ENV: production

jobs:
  deploy:
    environment: production
    env:
      # Nível job
      API_URL: https://api.exemplo.com
    
    steps:
      - env:
          # Nível step
          DEBUG: true
        run: |
          echo "NODE_ENV=$NODE_ENV"
          echo "API_URL=$API_URL"
          echo "DEBUG=$DEBUG"
```

## Environments

### Configurar Environment
```yaml
# Settings → Environments → New environment

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.exemplo.com
    
    steps:
      - run: echo "Deploying to production"
```

### Protection Rules
- Required reviewers
- Wait timer
- Deployment branches
- Environment secrets

## Artifacts

### Upload Artifacts
```yaml
- name: Build application
  run: npm run build

- name: Upload build artifacts
  uses: actions/upload-artifact@v3
  with:
    name: build-files
    path: |
      dist/
      build/
      !build/**/*.map
    retention-days: 7
```

### Download Artifacts
```yaml
- name: Download artifacts
  uses: actions/download-artifact@v3
  with:
    name: build-files
    path: ./dist
```

## Cache

### Cache Dependencies
```yaml
- name: Cache node modules
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Cache Docker layers
  uses: actions/cache@v3
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-buildx-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-buildx-
```

## Debugging

### Debug Mode
```yaml
# Habilitar debug logging
secrets:
  ACTIONS_RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

### Debug com tmate
```yaml
- name: Setup tmate session
  if: ${{ github.event_name == 'workflow_dispatch' }}
  uses: mxschmitt/action-tmate@v3
```

### Logs e Outputs
```yaml
- name: Debug info
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
    echo "Repository: ${{ github.repository }}"
    echo "Workspace: ${{ github.workspace }}"
```

## Best Practices

### 1. Pin Actions Versions
```yaml
# Bom - versão específica
uses: actions/checkout@v3

# Melhor - SHA commit
uses: actions/checkout@f43a0e5ff2bd294095638e18286ca9a3d1956744

# Ruim - branch
uses: actions/checkout@main
```

### 2. Timeouts
```yaml
jobs:
  test:
    timeout-minutes: 10
    steps:
      - timeout-minutes: 2
        run: npm test
```

### 3. Concorrência
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### 4. Dependabot para Actions
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 5. Reusable Workflows
```yaml
# .github/workflows/reusable.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string

# Usar em outro workflow
jobs:
  deploy:
    uses: ./.github/workflows/reusable.yml
    with:
      environment: production
```

## Limites e Cotas

### GitHub Free
- 2.000 minutos/mês (Linux)
- 20 concurrent jobs
- 500MB artifacts
- 14 dias retenção

### GitHub Pro
- 3.000 minutos/mês
- 40 concurrent jobs
- 1GB artifacts
- 90 dias retenção

## Troubleshooting Comum

### Problema: Permission denied
```yaml
# Solução
permissions:
  contents: read
  packages: write
```

### Problema: Cannot find module
```yaml
# Solução - cache correto
- uses: actions/setup-node@v3
  with:
    cache: 'npm'
- run: npm ci  # não npm install
```

### Problema: Secrets não funcionam em PR de fork
```yaml
# Solução - use pull_request_target com cuidado
on:
  pull_request_target:
    types: [opened, synchronize]
```

---

💡 **Próximo**: Pipeline multi-estágio com build, test e deploy!