# Conteúdo Teórico - Docker Compose

## 1. O que é Docker Compose?

### Definição
Docker Compose é uma ferramenta para definir e executar aplicações multi-container. Com um arquivo YAML, você configura todos os serviços da aplicação e, com um único comando, cria e inicia todos os serviços.

### Problema que resolve
```bash
# Sem Compose - múltiplos comandos
docker network create app-net
docker run -d --name db --network app-net -v db-data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=senha postgres
docker run -d --name redis --network app-net redis
docker run -d --name app --network app-net -p 80:80 -e DB_HOST=db -e REDIS_HOST=redis myapp

# Com Compose - um comando
docker-compose up -d
```

### Benefícios
- **Reprodutibilidade:** Mesmo ambiente em qualquer máquina
- **Simplicidade:** Um arquivo define tudo
- **Versionamento:** Infraestrutura como código
- **Desenvolvimento:** Ambientes locais idênticos
- **Documentação:** O arquivo é a documentação

---

## 2. Sintaxe YAML

### Estrutura básica
```yaml
# Comentário
chave: valor
lista:
  - item1
  - item2
objeto:
  propriedade1: valor1
  propriedade2: valor2
```

### Regras importantes
- **Indentação:** Use espaços, não tabs
- **Consistência:** Sempre 2 ou 4 espaços
- **Dois pontos:** Sempre espaço após `:`
- **Strings:** Aspas opcionais (exceto valores especiais)
- **Booleanos:** `true`, `false`, `yes`, `no`

### Exemplo prático
```yaml
version: '3.8'  # String

services:       # Objeto
  web:          # Nome do serviço
    image: nginx:alpine
    ports:      # Lista
      - "80:80"
    environment:  # Objeto ou lista
      DEBUG: "false"  # String (não booleano)
      WORKERS: 4      # Número
```

---

## 3. Estrutura do docker-compose.yml

### Seções principais
```yaml
version: '3.8'  # Versão do formato

services:       # Definição dos containers
  web:
    # configurações do serviço
  db:
    # configurações do serviço

networks:       # Redes customizadas (opcional)
  frontend:
  backend:

volumes:        # Volumes nomeados (opcional)
  db-data:
  uploads:

configs:        # Configurações externas (opcional)
secrets:        # Secrets (opcional)
```

---

## 4. Configuração de Serviços

### Opções essenciais
```yaml
services:
  app:
    # Imagem ou build
    image: node:18-alpine
    # OU
    build:
      context: .
      dockerfile: Dockerfile.prod
    
    # Nome do container
    container_name: my-app
    
    # Portas
    ports:
      - "3000:3000"     # host:container
      - "127.0.0.1:8080:8080"  # IP específico
    
    # Variáveis de ambiente
    environment:
      NODE_ENV: production
      DB_HOST: postgres
    # OU arquivo
    env_file:
      - .env
      - .env.production
    
    # Volumes
    volumes:
      - ./src:/app/src             # Bind mount
      - app-data:/data             # Volume nomeado
      - /app/node_modules          # Volume anônimo
    
    # Redes
    networks:
      - backend
      - frontend
    
    # Dependências
    depends_on:
      - db
      - redis
    
    # Restart policy
    restart: unless-stopped
    
    # Comando
    command: npm start
    
    # Working directory
    working_dir: /app
    
    # Usuário
    user: "1000:1000"
```

### Health check
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      # OU
      test: curl -f http://localhost/health || exit 1
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Deploy (Swarm/Compose v3+)
```yaml
services:
  web:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

---

## 5. Networks

### Tipos de rede
```yaml
networks:
  # Rede padrão bridge
  frontend:
    driver: bridge
  
  # Rede customizada
  backend:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: br-backend
    ipam:
      config:
        - subnet: 172.20.0.0/16
  
  # Rede externa (já existe)
  existing-net:
    external: true
    name: my-existing-network
```

### Uso nos serviços
```yaml
services:
  web:
    networks:
      - frontend
      - backend
    # OU com alias
    networks:
      backend:
        aliases:
          - api
          - web-api
```

---

## 6. Volumes

### Tipos de volumes
```yaml
volumes:
  # Volume nomeado simples
  db-data:
  
  # Volume com driver específico
  nfs-data:
    driver: local
    driver_opts:
      type: nfs
      o: addr=10.0.0.1,rw
      device: ":/path/to/dir"
  
  # Volume externo
  existing-vol:
    external: true
    name: my-existing-volume
```

### Uso nos serviços
```yaml
services:
  db:
    volumes:
      # Volume nomeado
      - db-data:/var/lib/postgresql/data
      
      # Bind mount
      - ./backup:/backup
      
      # Volume read-only
      - ./config:/etc/config:ro
      
      # Volume com opções
      - type: volume
        source: db-data
        target: /data
        volume:
          nocopy: true
```

---

## 7. Variáveis de Ambiente

### Métodos de definição
```yaml
services:
  app:
    # Direto no compose
    environment:
      NODE_ENV: production
      PORT: 3000
    
    # De arquivo .env
    env_file:
      - .env
    
    # Interpolação
    environment:
      DATABASE_URL: postgres://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}
```

### Arquivo .env
```env
# .env
DB_USER=admin
DB_PASS=secret123
DB_NAME=myapp
```

### Precedência
1. Compose file `environment:`
2. Shell environment variables
3. Environment file `.env`
4. Dockerfile ENV
5. Valores padrão no Compose

---

## 8. Comandos Docker Compose

### Comandos básicos
```bash
# Subir serviços
docker-compose up          # Foreground
docker-compose up -d       # Background
docker-compose up --build  # Rebuild images

# Parar serviços
docker-compose stop        # Para containers
docker-compose down        # Para e remove
docker-compose down -v     # Remove volumes também

# Status
docker-compose ps          # Lista containers
docker-compose logs        # Ver logs
docker-compose logs -f web # Logs de um serviço

# Executar comandos
docker-compose exec web sh           # Shell no container
docker-compose run web npm test      # Novo container temporário

# Build
docker-compose build              # Build all
docker-compose build --no-cache  # Sem cache

# Scale
docker-compose up -d --scale web=3   # 3 instâncias do web
```

### Comandos úteis
```bash
# Validar arquivo
docker-compose config

# Ver configuração processada
docker-compose config --resolve-image-digests

# Pull images
docker-compose pull

# Reiniciar
docker-compose restart

# Pausar/Despausar
docker-compose pause
docker-compose unpause

# Ver processos
docker-compose top

# Remover containers parados
docker-compose rm
```

---

## 9. Multi-stage e Override

### Arquivos múltiplos
```bash
# docker-compose.yml - base
# docker-compose.override.yml - dev (automático)
# docker-compose.prod.yml - produção

# Desenvolvimento (usa override automaticamente)
docker-compose up

# Produção (especifica arquivos)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Exemplo override
```yaml
# docker-compose.yml
services:
  web:
    image: myapp

# docker-compose.override.yml
services:
  web:
    build: .
    volumes:
      - .:/app
    environment:
      DEBUG: "true"
```

---

## 10. Boas Práticas

### Organização
```
projeto/
├── docker-compose.yml       # Principal
├── docker-compose.override.yml  # Dev
├── docker-compose.prod.yml  # Prod
├── .env                     # Variáveis locais
├── .env.example            # Template
├── nginx/
│   └── nginx.conf
├── postgres/
│   └── init.sql
└── app/
    ├── Dockerfile
    └── src/
```

### Dicas importantes
1. **Use versão específica:** `version: '3.8'`
2. **Networks explícitas:** Não dependa da default
3. **Volumes nomeados:** Facilita backup
4. **Health checks:** Para dependências
5. **Restart policies:** Para resiliência
6. **.env no .gitignore:** Segurança
7. **Build args:** Para builds flexíveis
8. **Labels:** Para organização

### Exemplo completo otimizado
```yaml
version: '3.8'

# Anchor YAML para reutilizar configurações comuns
x-common-variables: &common-variables
  TZ: America/Sao_Paulo
  LOG_LEVEL: info

services:
  db:
    image: postgres:15-alpine
    environment:
      <<: *common-variables
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build:
      context: .
      args:
        NODE_ENV: ${NODE_ENV:-production}
    depends_on:
      db:
        condition: service_healthy
    environment:
      <<: *common-variables
      DATABASE_URL: postgres://postgres:${DB_PASSWORD}@db:5432/app
    networks:
      - backend
      - frontend
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.web.rule=Host(`app.local`)"

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # Sem acesso externo

volumes:
  postgres-data:
    driver: local
```

---

## Recursos Adicionais

- [Documentação Oficial](https://docs.docker.com/compose/)
- [Compose file reference](https://docs.docker.com/compose/compose-file/)
- [Best practices](https://docs.docker.com/develop/dev-best-practices/)
- [Awesome Compose](https://github.com/docker/awesome-compose)