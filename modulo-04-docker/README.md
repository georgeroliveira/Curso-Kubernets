# Módulo 04 - Docker Fundamentos

**Versão 1.0 • DevOps Bootcamp 2025**

---

## 🚀 O que você vai aprender

Neste módulo, você aprenderá a **empacotar e executar o TaskManager em containers Docker**, tornando sua aplicação **portável, previsível e fácil de implantar** em qualquer ambiente DevOps.

**Ao final deste módulo, você será capaz de:**

*   Compreender a diferença e as vantagens dos Containers em relação às Máquinas Virtuais.
*   Dominar os conceitos de **Imagem**, **Container**, **Dockerfile**, **Volume** e **Network**.
*   Criar **Dockerfiles eficientes** e otimizados, utilizando boas práticas como *multi-stage builds*.
*   Gerenciar o ciclo de vida de containers e volumes usando comandos Docker essenciais.
*   Preparar o projeto **TaskManager** para o próximo passo: a orquestração multi-container.

---

## 💡 Por que isso é importante

O Docker é a tecnologia fundamental que permite a **orquestração de containers** com ferramentas como o Kubernetes.

| Problema Resolvido | Benefício para o Curso |
| :--- | :--- |
| **"Funciona na minha máquina"** | Garante um ambiente idêntico em desenvolvimento, testes e produção. |
| **Configuração Manual** | Empacota todas as dependências junto com a aplicação, eliminando erros de instalação. |
| **Isolamento** | Permite que múltiplas aplicações rodem no mesmo servidor sem conflitos de portas ou bibliotecas. |
| **Base para Kubernetes** | O domínio do Docker é o pré-requisito técnico mais importante para entender a orquestração. |

---

## 🛠️ Ambiente de Trabalho

Você utilizará o **VSCode no seu computador** conectado via **Remote SSH na VM Ubuntu**, onde o Docker estará instalado.

**Fluxo de Trabalho:**

1.  Você edita o **Dockerfile** e o código na VM via VSCode.
2.  O Docker roda **dentro da VM**, simulando um servidor remoto de produção.
3.  Você testa a aplicação acessando o IP da VM.

---

## ✅ Pré-requisitos

Certifique-se de que os seguintes itens estão configurados **antes de iniciar o Lab 1**:

### Na sua VM Ubuntu
*   [ ] Docker instalado e testado na VM Ubuntu 24.04.
*   [ ] TaskManager do Módulo 3 funcionando.
*   [ ] Git configurado e projeto versionado.
*   [ ] Conhecimento básico de terminal Linux.

### Verificação Rápida do Docker na VM

```bash
# Conecte na VM e execute:
docker --version
docker ps
docker run hello-world
```

**Saída esperada do último comando:** `Hello from Docker! This message shows that your installation appears to be working correctly.`

---

## 📚 Estrutura do Módulo (4 Horas)

O módulo é composto por 6 Labs práticos e progressivos, utilizando o projeto **TaskManager**.

| Lab | Foco | Duração | Habilidades Adquiridas |
| :---: | :--- | :--- | :--- |
| **1** | **Primeiro Dockerfile** | 30 min | Criação de um Dockerfile básico para containerizar o TaskManager. |
| **2** | **Execução e Debug** | 45 min | Domínio dos comandos `docker run`, `ps`, `logs` e `exec`. |
| **3** | **Volumes e Persistência** | 45 min | Configuração de volumes para garantir que os dados da aplicação persistam. |
| **4** | **Otimização** | 45 min | Aplicação de boas práticas como `.dockerignore` e ordenação de comandos. |
| **5** | **Multi-stage Build** | 30 min | Implementação de *multi-stage builds* para imagens menores e mais seguras. |
| **6** | **Preparação para Compose** | 30 min | Conclusão do TaskManager containerizado, pronto para o próximo módulo. |

---

## 📝 O Projeto TaskManager: Evolução

O TaskManager evolui em cada módulo, aplicando os conceitos aprendidos.

| Módulo | Evolução do Projeto | Conceito de Kubernetes Relacionado |
| :---: | :--- | :--- |
| **03** | Código versionado em Git | IaC (Infrastructure as Code) |
| **04** | **TaskManager containerizado** | **Pods e Imagens Otimizadas** |
| **05** | Stack multi-container com Compose | Orquestração Local (Preparação para Deployments) |
| **06** | Automatizar deploy com Ansible | Provisionamento e Configuração |
| **07** | Pipeline CI/CD completo | CI/CD no Kubernetes |
| **08** | Observabilidade com Prometheus + Grafana | Monitoramento e Logs de Cluster |

---

## 💡 Dicas e Boas Práticas

### Boas Práticas Docker
*   Crie imagens pequenas (use `python:3.11-slim`).
*   Sempre utilize `.dockerignore`.
*   Nomeie suas imagens com `user/projeto:versao`.
*   Teste suas builds com `docker run` antes de enviar ao registry.
*   Remova recursos não utilizados com `docker system prune`.

### Mindset DevOps
*   Containers são **imutáveis**.
*   Dados persistentes vão em **volumes**.
*   Um processo por container.
*   Logs vão para `stdout`/`stderr`.

---

## 🛠️ Comandos Docker Essenciais

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

# Limpeza
docker system prune
```

---

## ➡️ Próximo Passo

**Conecte no VSCode via Remote SSH** e abra o arquivo **`labs.md`** para iniciar o primeiro lab prático.

---

**Versão:** 1.0  
**Instrutor:** DevOps Bootcamp Team  
**Próximo módulo:** Docker Compose - Orquestração Multi-Container
