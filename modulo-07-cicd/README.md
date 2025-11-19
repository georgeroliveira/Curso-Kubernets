# Módulo 07 - CI/CD com GitHub Actions

Este módulo implementa:

- CI (testes + build)
- CD (deploy automatizado)
- Security scanning
- Deploy via SSH + Docker Compose

A stack completa segue o fluxo:

1. push → CI
2. tag v* → CD
3. nightly → Security Scan

Inclui:
- Dockerfile
- docker-compose.prod.yml
- Scripts de deploy e rollback
