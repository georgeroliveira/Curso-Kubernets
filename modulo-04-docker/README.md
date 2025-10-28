# Módulo 04 - Docker Fundamentos  
Versão 1.0 • DevOps Bootcamp 2025

## O que você vai aprender

Neste módulo, você aprenderá a **empacotar e executar o TaskManager em containers Docker**, tornando sua aplicação **portável, previsível e fácil de implantar** em qualquer ambiente DevOps.

Você vai conquistar:
- Containerizar o TaskManager em Docker  
- Dominar comandos Docker essenciais  
- Construir imagens eficientes  
- Preparar o projeto para orquestração (Docker Compose)

---

## Pré-requisitos

Antes da aula, você precisa ter:

### Na VM Ubuntu
- Docker instalado e testado na VM Ubuntu 24.04
- TaskManager do Módulo 3 funcionando
- Git configurado e projeto versionado
- Conhecimento básico de terminal Linux

### Verificar Docker

```bash
docker --version
docker ps
docker run hello-world
```

**Saída esperada:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## Como estudar este módulo

1. **Verificação (15 min):** Testar Docker na VM
2. **Teoria rápida (30 min):** Conceitos e terminologia essencial
3. **Prática (2h45):** Labs progressivos e guiados
4. **Otimização (30 min):** Dockerfile avançado e boas práticas

---

## Estrutura do Módulo

```
modulo-04-docker/
├── README.md              # Você está aqui
├── labs.md                # Exercícios práticos (foco principal)
└── conteudo-docker.md     # Referência teórica (consulta)
```

---

## Cronograma de 4 horas

| Tempo     | Atividade | Objetivo                                   |
| --------- | --------- | ------------------------------------------ |
| 0:00-0:15 | Setup     | Verificar Docker na VM                     |
| 0:15-0:45 | Lab 1     | Criar o primeiro Dockerfile do TaskManager |
| 0:45-1:30 | Lab 2     | Executar e debugar containers              |
| 1:30-2:15 | Lab 3     | Trabalhar com volumes para persistência    |
| 2:15-3:00 | Lab 4     | Otimizar o Dockerfile                      |
| 3:00-3:30 | Lab 5     | Implementar multi-stage build              |
| 3:30-4:00 | Lab 6     | Preparar para Docker Compose               |

---

## Boas Práticas DevOps com Docker

- Crie imagens pequenas (use `python:3.11-slim`)
- Sempre utilize `.dockerignore`
- Nomeie suas imagens com `user/projeto:versao`
- Teste suas builds com `docker run` antes de enviar ao registry
- Remova recursos não utilizados com `docker system prune`

---

## Evolução do TaskManager

### Módulo 3 (anterior)
- TaskManager Flask funcional
- Código versionado em Git
- Interface web completa
- Health checks e logs

### Módulo 4 (atual)
- TaskManager containerizado
- Dockerfile otimizado
- Imagem Docker funcional
- Volumes para persistência

### Módulo 5 (próximo)
- Stack multi-container
- PostgreSQL + Redis
- Orquestração com Docker Compose

---

## Checklist de Conclusão

Ao final do módulo, você deve ter:

- TaskManager rodando em container
- Dockerfile eficiente criado
- Volumes configurados para dados
- Imagem otimizada (multi-stage)
- Projeto preparado para Docker Compose

---

## Comandos Docker Essenciais

Você dominará estes comandos durante os labs:

```bash
# Build de imagem
docker build -t taskmanager .

# Executar container
docker run -p 5000:5000 taskmanager

# Listar containers
docker ps

# Ver logs
docker logs <container_id>

# Entrar no container
docker exec -it <container_id> bash

# Criar volume
docker volume create data

# Limpeza
docker system prune
```

---

## Resultado Final

Após este módulo, você terá:

1. Um TaskManager portável e executável em qualquer ambiente
2. Experiência prática com containers Docker
3. Um Dockerfile otimizado e pronto para produção
4. Base sólida para o próximo módulo: orquestração multi-container com Docker Compose

---

## Material de Apoio

Durante a aula, você terá acesso a:

- **conteudo-docker.md:** Conceitos teóricos de Docker
- **labs.md:** Instruções passo a passo de cada lab
- **troubleshooting.md:** Soluções para erros comuns

Todos os arquivos estarão disponíveis no repositório do curso.

---

## Dicas para o Sucesso

### Durante os Labs
- Leia cada passo com atenção antes de executar
- Valide cada checkpoint antes de avançar
- Entenda o "por quê" de cada comando
- Pergunte quando tiver dúvidas

### Boas Práticas Docker
- Sempre use .dockerignore
- Imagens pequenas = deploys rápidos
- Teste localmente antes de fazer push
- Nomeie imagens e tags claramente

### Mindset DevOps
- Containers são imutáveis
- Dados persistentes vão em volumes
- Um processo por container
- Logs vão para stdout/stderr

---

## Troubleshooting Rápido

### Docker não está instalado

```bash
# Instalar Docker na VM Ubuntu
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
# Fazer logout e login novamente
```

### Permissão negada

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
# Fazer logout e login
```

### Porta já em uso

```bash
# Verificar processo usando porta
sudo lsof -i :5000
# Parar container
docker stop <container_id>
```

---

## Próximo Passo

**Conecte no VSCode via Remote SSH** e abra o arquivo **`labs.md`** para iniciar o primeiro lab prático.

Lembre-se: você está trabalhando remotamente na VM, todos os comandos Docker rodam lá.

---

**Versão:** 1.0  
**Data:** 2025  
**Instrutor:** DevOps Bootcamp Team  
**Próximo módulo:** Docker Compose - Orquestração Multi-Container