# Índice dos Labs - Módulo 05

## Ordem de Execução

### Lab 01 - Stack Multi-Container
**Arquivo:** labs_01.md  
**Duração:** 60 minutos  
**Conteúdo:**
- Criar docker-compose.yml
- PostgreSQL + Redis + Flask
- Volumes e redes

### Lab 02 - Nginx e Escalabilidade  
**Arquivo:** labs_02.md  
**Duração:** 70 minutos  
**Conteúdo:**
- Nginx como load balancer
- 3 instâncias da aplicação
- Alta disponibilidade

### Lab 03 - Produção Ready
**Arquivo:** labs_03.md  
**Duração:** 60 minutos  
**Conteúdo:**
- Health checks avançados
- Scripts de backup/deploy
- Logs estruturados

---

## Documentação de Apoio

| Arquivo | Conteúdo |
|---------|----------|
| **Arquitetura.md** | Diagramas detalhados da stack |
| **Troubleshooting.md** | Top 15 problemas e soluções |

## Código de Referência

Se travar em algum lab, consulte:
```
../projeto-taskmanager/
├── docker-compose.yml    # Configuração completa
├── app.py                # Código da aplicação
├── nginx/nginx.conf      # Load balancer
└── scripts/              # Automação
```

## Teoria

Documentação completa em:
```
../teoria/
├── conteudo_compose_final.md  # Referência Docker Compose
└── deploy_final.md            # Estratégias de deploy/CI/CD
```

---

## Tempo Total

- **Labs práticos:** ~190 minutos (3h10min)
- **Leitura teoria:** ~60 minutos
- **Total:** ~4 horas

---

**Dica:** Comece pelo Lab 01 e siga a ordem. Boa sorte!
