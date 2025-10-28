# Pipeline Multi-estágio: Build → Test → Deploy

## Arquitetura de Pipeline Multi-estágio

Um pipeline multi-estágio divide o processo de CI/CD em fases distintas, cada uma com responsabilidades específicas.

```mermaid
graph LR
    A[Source Code] --> B[Build Stage]
    B --> C[Test Stage]
    C --> D[Security Stage]
    D --> E[Deploy Staging]
    E --> F[Deploy Production]
    
    B --> G[Artifacts]
    C --> H[Test Reports]
    D --> I[Security Reports]
```

## Estágios Fundamentais

### 1. Build Stage
**Objetivo**: Compilar código e criar artifacts

```yaml
build:
  stage: build
  script:
    - Validar sintaxe
    - Instalar dependências
    - Compilar/Transpilar código
    - Criar bundles
    - Gerar artifacts
  artifacts:
    - Binários
    - Imagens Docker
    - Pacotes
```

### 2. Test Stage
**Objetivo**: Garantir qualidade do código

```yaml
test:
  stage: test
  script:
    - Unit tests
    - Integration tests
    - Coverage analysis
    - Code quality checks
  reports:
    - Coverage reports
    - Test results
    - Quality metrics
```

### 3. Deploy Stage
**Objetivo**: Entregar aplicação aos ambientes

```yaml
deploy:
  stage: deploy
  script:
    - Deploy staging
    - Smoke tests
    - Deploy production
    - Health checks
  environments:
    - Development
    - Staging
    - Production
```

## Pipeline Completo com GitHub Actions

### Estrutura do Projeto
```
projeto/
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── src/
│   └── app.js
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
├── docker-compose.yml
└── package.json
```

### Pipeline YAML Completo

```yaml
name: Complete CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  NODE_VERSION: '16'

jobs:
  # =====================================================
  # STAGE 1: Build
  # =====================================================
  build:
    name: Build Application
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
      image-tag: ${{ steps.meta.outputs.tags }}
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: 📝 Generate version
        id: version
        run: |
          VERSION=$(date +%Y%m%d)-${{ github.run_number }}-$(git rev-parse --short HEAD)
          echo "version=$VERSION" >> $GITHUB_OUTPUT
          echo "Version: $VERSION"
      
      - name: 🔧 Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: 📦 Install dependencies
        run: |
          npm ci --prefer-offline --no-audit
          npm run validate
      
      - name: 🏗️ Build application
        run: |
          npm run build
          echo "${{ steps.version.outputs.version }}" > dist/version.txt
      
      - name: 📤 Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-${{ steps.version.outputs.version }}
          path: |
            dist/
            package.json
            package-lock.json
          retention-days: 7
      
      - name: 🐳 Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: 🔐 Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: 🏷️ Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix={{branch}}-
            type=raw,value=${{ steps.version.outputs.version }}
            type=raw,value=latest,enable={{is_default_branch}}
      
      - name: 🐳 Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            VERSION=${{ steps.version.outputs.version }}
            BUILD_DATE=${{ github.event.head_commit.timestamp }}

  # =====================================================
  # STAGE 2: Test
  # =====================================================
  test-unit:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: build
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3
      
      - name: 🔧 Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: 📦 Install dependencies
        run: npm ci
      
      - name: 🧪 Run unit tests
        run: |
          npm run test:unit -- --coverage --coverageReporters=json --coverageReporters=lcov --coverageReporters=text
      
      - name: 📊 Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/lcov.info
          fail_ci_if_error: false
      
      - name: 📤 Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: unit-test-results
          path: |
            coverage/
            test-results/
  
  test-integration:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: build
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3
      
      - name: 🔧 Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: 📦 Install dependencies
        run: npm ci
      
      - name: 🗄️ Run database migrations
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/testdb
        run: npm run migrate
      
      - name: 🧪 Run integration tests
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
        run: npm run test:integration
      
      - name: 📤 Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: integration-test-results
          path: test-results/

  test-e2e:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: build
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3
      
      - name: 🐳 Start services with Docker Compose
        run: |
          docker-compose -f docker-compose.test.yml up -d
          sleep 10
          docker-compose -f docker-compose.test.yml ps
      
      - name: 🎭 Install Playwright
        run: |
          npm ci
          npx playwright install --with-deps
      
      - name: 🧪 Run E2E tests
        run: |
          npm run test:e2e
      
      - name: 📤 Upload Playwright report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
      
      - name: 🧹 Cleanup
        if: always()
        run: docker-compose -f docker-compose.test.yml down

  # =====================================================
  # STAGE 3: Security
  # =====================================================
  security:
    name: Security Scanning
    runs-on: ubuntu-latest
    needs: build
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3
      
      - name: 🔒 Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.build.outputs.version }}
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: 📤 Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: 🔍 SAST - SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      
      - name: 🔐 Check for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
      
      - name: 📋 Dependency check
        run: |
          npm audit --audit-level=moderate
          npm outdated || true

  # =====================================================
  # STAGE 4: Deploy to Staging
  # =====================================================
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build, test-unit, test-integration, security]
    if: github.ref == 'refs/heads/develop' || github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.exemplo.com
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3
      
      - name: 📥 Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: build-${{ needs.build.outputs.version }}
          path: ./dist
      
      - name: 🔐 Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: 🚀 Deploy to ECS
        run: |
          # Update task definition
          aws ecs register-task-definition \
            --family my-app-staging \
            --container-definitions '[{
              "name": "app",
              "image": "${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.build.outputs.version }}",
              "memory": 512,
              "cpu": 256,
              "essential": true
            }]'
          
          # Update service
          aws ecs update-service \
            --cluster staging-cluster \
            --service my-app-service \
            --task-definition my-app-staging
      
      - name: 🧪 Run smoke tests
        run: |
          npm run test:smoke -- --url=https://staging.exemplo.com
      
      - name: 📢 Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Staging Deployment: ${{ job.status }}
            Version: ${{ needs.build.outputs.version }}
            URL: https://staging.exemplo.com
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()

  # =====================================================
  # STAGE 5: Deploy to Production
  # =====================================================
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build, deploy-staging]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://app.exemplo.com
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3
      
      - name: 🔐 Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.PROD_AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.PROD_AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: 📸 Create backup
        run: |
          # Backup current version
          aws ecs describe-services \
            --cluster production-cluster \
            --services my-app-service \
            --query 'services[0].taskDefinition' \
            --output text > backup-task-definition.txt
      
      - name: 🚀 Blue-Green Deployment
        run: |
          # Deploy to blue environment
          ./scripts/deploy-blue-green.sh \
            --cluster production-cluster \
            --service my-app-service \
            --image "${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.build.outputs.version }}" \
            --environment blue
          
          # Health check
          ./scripts/health-check.sh --url https://blue.exemplo.com
          
          # Switch traffic
          ./scripts/switch-traffic.sh --to blue
          
          # Monitor for 5 minutes
          ./scripts/monitor.sh --duration 300
      
      - name: 🧪 Run production tests
        run: |
          npm run test:production -- --url=https://app.exemplo.com
      
      - name: 📊 Update monitoring dashboards
        run: |
          curl -X POST ${{ secrets.GRAFANA_URL }}/api/annotations \
            -H "Authorization: Bearer ${{ secrets.GRAFANA_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{
              "text": "Deployment: ${{ needs.build.outputs.version }}",
              "tags": ["deployment", "production"]
            }'
      
      - name: 📢 Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            🚀 Production Deployment: ${{ job.status }}
            Version: ${{ needs.build.outputs.version }}
            URL: https://app.exemplo.com
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()

  # =====================================================
  # STAGE 6: Post-Deploy Validation
  # =====================================================
  validate-deployment:
    name: Validate Deployment
    runs-on: ubuntu-latest
    needs: [deploy-production]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3
      
      - name: 🔍 Performance testing
        run: |
          npm install -g lighthouse
          lighthouse https://app.exemplo.com \
            --output=json \
            --output-path=./lighthouse-report.json \
            --chrome-flags="--headless"
      
      - name: 📊 Check metrics
        run: |
          # Query Prometheus/Grafana for key metrics
          ./scripts/check-metrics.sh \
            --error-rate-threshold 1 \
            --response-time-threshold 200
      
      - name: 🔄 Rollback if needed
        if: failure()
        run: |
          echo "⚠️ Validation failed, initiating rollback..."
          ./scripts/rollback.sh \
            --cluster production-cluster \
            --service my-app-service \
            --task-definition $(cat backup-task-definition.txt)
```

## Estratégias de Deploy

### Blue-Green Deployment
```yaml
# Dois ambientes idênticos
Blue (Produção atual) ← Tráfego
Green (Nova versão)

# Deploy
Green ← Deploy nova versão
Green ← Testes
Tráfego → Green
Blue ← Standby (rollback rápido)
```

### Canary Deployment
```yaml
# Deploy gradual
5% tráfego → Nova versão
Monitor métricas
25% tráfego → Nova versão
Monitor métricas
100% tráfego → Nova versão
```

### Rolling Deployment
```yaml
# Atualização incremental
Instance 1 → Nova versão
Instance 2 → Nova versão
Instance 3 → Nova versão
```

## Rollback Strategies

### Automatic Rollback
```yaml
- name: Deploy with auto-rollback
  run: |
    # Deploy
    ./deploy.sh
    
    # Monitor for 5 minutes
    if ! ./health-check.sh --duration 300; then
      echo "Health check failed, rolling back..."
      ./rollback.sh
      exit 1
    fi
```

### Manual Rollback
```yaml
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true

jobs:
  rollback:
    steps:
      - run: ./rollback.sh --version ${{ github.event.inputs.version }}
```

## Monitoring e Observability

### Métricas Importantes
- Build success rate
- Test pass rate
- Deployment frequency
- Lead time
- MTTR (Mean Time to Recovery)
- Change failure rate

### Dashboards
```yaml
# Grafana Dashboard JSON
{
  "dashboard": {
    "title": "CI/CD Pipeline Metrics",
    "panels": [
      {
        "title": "Build Success Rate",
        "targets": [
          {
            "expr": "rate(builds_total{status='success'}[1h])"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

1. **Fast Feedback**: Falhe rápido, notifique imediatamente
2. **Parallel Execution**: Execute testes em paralelo
3. **Cache Everything**: Dependencies, Docker layers, artifacts
4. **Progressive Deployment**: Staging → Canary → Production
5. **Automated Rollback**: Detecte e reverta falhas automaticamente
6. **Comprehensive Testing**: Unit → Integration → E2E → Performance
7. **Security First**: SAST, DAST, dependency scanning

---

💡 **Próximo**: Secrets management e estratégias de rollback!