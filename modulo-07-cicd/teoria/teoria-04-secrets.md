# Secrets Management e Estratégias de Rollback

## Parte 1: Secrets Management

### O que são Secrets?

Secrets são informações sensíveis que sua aplicação precisa mas não devem ser expostas:
- Senhas de banco de dados
- API keys
- Tokens de autenticação
- Certificados SSL
- Chaves SSH
- Variáveis de ambiente sensíveis

### ❌ O que NÃO fazer

```yaml
# NUNCA faça isso!
env:
  DATABASE_PASSWORD: "senha123"  # ❌ Hardcoded
  API_KEY: "sk-1234567890abcdef"  # ❌ Exposto no código
  
# Também não faça isso
- run: |
    mysql -u root -psenha123  # ❌ Senha no comando
    curl -H "Authorization: Bearer token123"  # ❌ Token exposto
```

### ✅ Como gerenciar Secrets corretamente

## GitHub Secrets

### Tipos de Secrets

1. **Repository Secrets**
   - Específicos do repositório
   - Acessíveis em todos os workflows

2. **Environment Secrets**
   - Específicos por ambiente (staging, production)
   - Requerem aprovação para ambientes protegidos

3. **Organization Secrets**
   - Compartilhados entre repositórios
   - Gerenciados no nível da organização

4. **Dependabot Secrets**
   - Usados pelo Dependabot
   - Para registries privados

### Configurando Secrets no GitHub

```bash
# Via GitHub UI
Settings → Secrets and variables → Actions → New repository secret

# Via GitHub CLI
gh secret set DATABASE_PASSWORD
gh secret set API_KEY < api-key.txt
gh secret list
```

### Usando Secrets nos Workflows

```yaml
name: Deploy with Secrets

env:
  # ✅ Secrets no nível do workflow
  GLOBAL_SECRET: ${{ secrets.GLOBAL_SECRET }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Secrets do environment
    
    steps:
      # ✅ Secret em variável de ambiente
      - name: Use database
        env:
          DB_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}
        run: |
          echo "Connecting to database..."
          # Senha não aparece nos logs
      
      # ✅ Secret em arquivo
      - name: Create config file
        run: |
          cat > config.json <<EOF
          {
            "api_key": "${{ secrets.API_KEY }}",
            "database": {
              "password": "${{ secrets.DB_PASSWORD }}"
            }
          }
          EOF
      
      # ✅ Multiple secrets
      - name: Deploy application
        env:
          DB_HOST: ${{ secrets.DB_HOST }}
          DB_USER: ${{ secrets.DB_USER }}
          DB_PASS: ${{ secrets.DB_PASS }}
          REDIS_URL: ${{ secrets.REDIS_URL }}
        run: |
          ./deploy.sh
```

### Secrets com Docker

```yaml
# Build com secrets
- name: Build Docker image with secrets
  uses: docker/build-push-action@v4
  with:
    context: .
    secrets: |
      "npm_token=${{ secrets.NPM_TOKEN }}"
      "github_token=${{ secrets.GITHUB_TOKEN }}"
    build-args: |
      API_KEY=${{ secrets.API_KEY }}

# Docker login
- name: Login to Docker Hub
  uses: docker/login-action@v2
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}

# Docker Compose com secrets
- name: Deploy with Docker Compose
  run: |
    cat > .env <<EOF
    DB_PASSWORD=${{ secrets.DB_PASSWORD }}
    JWT_SECRET=${{ secrets.JWT_SECRET }}
    STRIPE_KEY=${{ secrets.STRIPE_KEY }}
    EOF
    docker-compose up -d
    rm .env  # Limpar após uso
```

### SSH Keys

```yaml
- name: Setup SSH
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    ssh-keyscan -H ${{ secrets.HOST }} >> ~/.ssh/known_hosts

- name: Deploy via SSH
  run: |
    ssh user@${{ secrets.HOST }} "cd /app && git pull && docker-compose up -d"
    
# Ou usando action
- name: Deploy via SSH Action
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.HOST }}
    username: ${{ secrets.USERNAME }}
    key: ${{ secrets.SSH_KEY }}
    script: |
      cd /app
      docker-compose pull
      docker-compose up -d
```

## Vault e Secret Management Tools

### HashiCorp Vault Integration

```yaml
- name: Import Secrets from Vault
  uses: hashicorp/vault-action@v2
  with:
    url: https://vault.exemplo.com
    token: ${{ secrets.VAULT_TOKEN }}
    secrets: |
      secret/data/ci npm_token | NPM_TOKEN ;
      secret/data/ci docker_password | DOCKER_PASSWORD ;
      database/creds/readonly username | DB_USER ;
      database/creds/readonly password | DB_PASSWORD

- name: Use Vault secrets
  run: |
    echo "NPM_TOKEN=$NPM_TOKEN" >> .env
    echo "DB connection: $DB_USER@database"
```

### AWS Secrets Manager

```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@v2
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1

- name: Get secrets from AWS
  run: |
    DB_PASSWORD=$(aws secretsmanager get-secret-value \
      --secret-id prod/db/password \
      --query SecretString --output text)
    
    export DB_PASSWORD
    ./deploy.sh
```

## Segurança de Secrets

### 1. Rotação de Secrets

```yaml
# Workflow para rotação mensal
name: Rotate Secrets

on:
  schedule:
    - cron: '0 0 1 * *'  # Primeiro dia do mês

jobs:
  rotate:
    runs-on: ubuntu-latest
    steps:
      - name: Generate new passwords
        run: |
          NEW_PASSWORD=$(openssl rand -base64 32)
          echo "::add-mask::$NEW_PASSWORD"
          echo "NEW_PASSWORD=$NEW_PASSWORD" >> $GITHUB_ENV
      
      - name: Update database password
        run: |
          # Update no banco
          mysql -u admin -p${{ secrets.DB_ADMIN_PASS }} \
            -e "ALTER USER 'app'@'%' IDENTIFIED BY '$NEW_PASSWORD';"
      
      - name: Update GitHub secret
        run: |
          gh secret set DB_PASSWORD --body "$NEW_PASSWORD"
```

### 2. Audit e Compliance

```yaml
- name: Audit secrets usage
  run: |
    # Log de uso (sem expor valores)
    echo "Secret DB_PASSWORD foi usado por ${{ github.actor }}"
    echo "Workflow: ${{ github.workflow }}"
    echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### 3. Masking Sensitive Data

```yaml
- name: Mask sensitive output
  run: |
    # Adicionar máscara para output
    echo "::add-mask::${{ secrets.API_KEY }}"
    
    # Agora mesmo se printar, será mascarado
    echo "API Key is: ${{ secrets.API_KEY }}"
    # Output: API Key is: ***
```

## Parte 2: Estratégias de Rollback

### Tipos de Rollback

1. **Immediate Rollback**: Reverter imediatamente
2. **Gradual Rollback**: Reverter gradualmente
3. **Feature Flag Rollback**: Desabilitar feature
4. **Database Rollback**: Reverter migrations

### Implementação de Rollback Automático

```yaml
name: Deploy with Auto-Rollback

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Save current version
        run: |
          CURRENT_VERSION=$(kubectl get deployment app -o jsonpath='{.spec.template.spec.containers[0].image}')
          echo "CURRENT_VERSION=$CURRENT_VERSION" >> $GITHUB_ENV
      
      - name: Deploy new version
        run: |
          kubectl set image deployment/app app=${{ env.NEW_IMAGE }}
          kubectl rollout status deployment/app --timeout=300s
      
      - name: Health check
        id: health
        run: |
          for i in {1..10}; do
            if curl -f https://app.exemplo.com/health; then
              echo "Health check passed"
              exit 0
            fi
            echo "Attempt $i failed, waiting..."
            sleep 30
          done
          exit 1
        continue-on-error: true
      
      - name: Rollback if unhealthy
        if: steps.health.outcome == 'failure'
        run: |
          echo "🔴 Health check failed, rolling back..."
          kubectl set image deployment/app app=${{ env.CURRENT_VERSION }}
          kubectl rollout status deployment/app
          
          # Notificar time
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"⚠️ Deployment failed and was rolled back"}'
          
          exit 1
```

### Rollback Manual

```yaml
name: Manual Rollback

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true
        type: string
      environment:
        description: 'Environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    
    steps:
      - name: Validate version exists
        run: |
          if ! docker manifest inspect myapp:${{ github.event.inputs.version }}; then
            echo "Version ${{ github.event.inputs.version }} not found!"
            exit 1
          fi
      
      - name: Backup current state
        run: |
          kubectl get all -n app > backup-$(date +%s).yaml
      
      - name: Execute rollback
        run: |
          # Update deployment
          kubectl set image deployment/app \
            app=myapp:${{ github.event.inputs.version }} \
            -n app
          
          # Wait for rollout
          kubectl rollout status deployment/app -n app
          
          # Verify
          kubectl get pods -n app
          kubectl logs -l app=myapp -n app --tail=50
      
      - name: Verify rollback
        run: |
          # Test endpoints
          ./scripts/smoke-test.sh
          
          # Check metrics
          ./scripts/check-metrics.sh
```

### Blue-Green Rollback

```yaml
- name: Blue-Green Deployment with Rollback
  run: |
    # Deploy to green
    kubectl apply -f green-deployment.yaml
    
    # Test green
    if ! curl -f https://green.exemplo.com/health; then
      echo "Green deployment failed"
      kubectl delete -f green-deployment.yaml
      exit 1
    fi
    
    # Switch traffic to green
    kubectl patch service app -p '{"spec":{"selector":{"version":"green"}}}'
    
    # Monitor for 5 minutes
    sleep 300
    
    # Check error rate
    ERROR_RATE=$(curl -s https://metrics.exemplo.com/error_rate)
    if (( $(echo "$ERROR_RATE > 5" | bc -l) )); then
      echo "High error rate detected, rolling back to blue"
      kubectl patch service app -p '{"spec":{"selector":{"version":"blue"}}}'
      kubectl delete -f green-deployment.yaml
      exit 1
    fi
    
    # Success - remove blue
    kubectl delete -f blue-deployment.yaml
```

### Database Rollback

```yaml
- name: Database Migration with Rollback
  run: |
    # Backup database
    pg_dump $DATABASE_URL > backup-$(date +%s).sql
    
    # Run migrations
    npm run migrate:up
    
    # Test migrations
    if ! npm run test:db; then
      echo "Database tests failed, rolling back..."
      npm run migrate:down
      exit 1
    fi
```

### Feature Flag Rollback

```yaml
- name: Deploy with Feature Flags
  env:
    LAUNCHDARKLY_SDK_KEY: ${{ secrets.LAUNCHDARKLY_SDK_KEY }}
  run: |
    # Deploy new code
    ./deploy.sh
    
    # Enable feature flag gradually
    ld flags update new-feature \
      --variations '{"rules":[{"variation":0,"weight":10}]}'  # 10%
    
    sleep 300  # Monitor for 5 minutes
    
    # Check metrics
    if ./check-metrics.sh | grep -q "ERROR"; then
      echo "Disabling feature flag"
      ld flags update new-feature --on false
    else
      echo "Increasing rollout"
      ld flags update new-feature \
        --variations '{"rules":[{"variation":0,"weight":50}]}'  # 50%
    fi
```

## Monitoring para Rollback

### Métricas para Trigger de Rollback

```yaml
- name: Monitor and Rollback
  run: |
    # Definir thresholds
    MAX_ERROR_RATE=5
    MAX_RESPONSE_TIME=1000
    MIN_SUCCESS_RATE=95
    
    # Coletar métricas
    ERROR_RATE=$(curl -s http://prometheus:9090/api/v1/query \
      -d 'query=rate(http_requests_total{status=~"5.."}[5m])' \
      | jq .data.result[0].value[1])
    
    RESPONSE_TIME=$(curl -s http://prometheus:9090/api/v1/query \
      -d 'query=http_request_duration_seconds{quantile="0.95"}' \
      | jq .data.result[0].value[1])
    
    SUCCESS_RATE=$(curl -s http://prometheus:9090/api/v1/query \
      -d 'query=rate(http_requests_total{status=~"2.."}[5m])' \
      | jq .data.result[0].value[1])
    
    # Decidir rollback
    if (( $(echo "$ERROR_RATE > $MAX_ERROR_RATE" | bc -l) )) || \
       (( $(echo "$RESPONSE_TIME > $MAX_RESPONSE_TIME" | bc -l) )) || \
       (( $(echo "$SUCCESS_RATE < $MIN_SUCCESS_RATE" | bc -l) )); then
      echo "🚨 Metrics exceeded thresholds, rolling back!"
      ./rollback.sh
      exit 1
    fi
```

## Best Practices

### Secrets Management
1. **Nunca** commitar secrets no código
2. **Sempre** use variáveis de ambiente
3. **Rotacione** secrets regularmente
4. **Audite** uso de secrets
5. **Limite** acesso por environment
6. **Encripte** secrets em trânsito e em repouso

### Rollback Strategy
1. **Sempre** tenha um plano de rollback
2. **Automatize** detecção de falhas
3. **Teste** procedimentos de rollback
4. **Mantenha** backups antes de deploy
5. **Documente** processo de rollback
6. **Monitore** após rollback

## Scripts Úteis

### check-deployment-health.sh
```bash
#!/bin/bash
set -e

URL=${1:-https://app.exemplo.com}
MAX_RETRIES=10
RETRY_DELAY=30

for i in $(seq 1 $MAX_RETRIES); do
  echo "Health check attempt $i/$MAX_RETRIES"
  
  # Check HTTP status
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL/health)
  
  if [ $HTTP_STATUS -eq 200 ]; then
    echo "✅ Health check passed"
    
    # Additional checks
    if curl -s $URL/metrics | grep -q "app_healthy 1"; then
      echo "✅ Metrics check passed"
      exit 0
    fi
  fi
  
  echo "Health check failed, waiting ${RETRY_DELAY}s..."
  sleep $RETRY_DELAY
done

echo "❌ Health check failed after $MAX_RETRIES attempts"
exit 1
```

### rollback.sh
```bash
#!/bin/bash
set -e

ENVIRONMENT=${1:-production}
VERSION=${2:-previous}

echo "🔄 Starting rollback to $VERSION in $ENVIRONMENT"

# Get previous version if not specified
if [ "$VERSION" == "previous" ]; then
  VERSION=$(kubectl get deployment app -o json | \
    jq -r '.metadata.annotations."deployment.kubernetes.io/revision-1"')
fi

# Execute rollback
kubectl rollout undo deployment/app --to-revision=$VERSION

# Wait for rollback
kubectl rollout status deployment/app

# Verify
./check-deployment-health.sh

echo "✅ Rollback completed successfully"

# Notify team
curl -X POST $SLACK_WEBHOOK \
  -H 'Content-Type: application/json' \
  -d "{\"text\":\"🔄 Rollback to $VERSION completed in $ENVIRONMENT\"}"
```

---

💡 **Conclusão**: Secrets bem gerenciados e rollback eficiente são fundamentais para CI/CD seguro e confiável!