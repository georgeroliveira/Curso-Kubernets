# Módulo 03 - Git do Zero ao Pull Request

**Versão 2.1 • DevOps Bootcamp 2025**

---

## 🚀 O que você vai aprender

Neste módulo, você aprenderá a **versionar código e configurações como um profissional DevOps**. Utilizaremos o projeto **TaskManager** como base para aplicar o Git em um fluxo de trabalho real, preparando o projeto para as etapas de containerização e orquestração.

**Ao final deste módulo, você será capaz de:**

*   Dominar os comandos essenciais do Git para o dia a dia.
*   Trabalhar com **Branches** para desenvolver novas funcionalidades com segurança.
*   Colaborar em equipe utilizando o fluxo de **Fork e Pull Request (PR)** no GitHub.
*   Versionar configurações de infraestrutura (IaC), e não apenas código de aplicação.

---

## 💡 Por que isso é importante

O Git é a **espinha dorsal** de qualquer pipeline de DevOps. O domínio desta ferramenta é um requisito obrigatório no mercado de trabalho e essencial para o sucesso deste curso.

| Aspecto | Relevância |
| :--- | :--- |
| **Mercado de Trabalho** | 100% das empresas de tecnologia utilizam Git. O fluxo de Pull Request é a principal forma de colaboração e é avaliado em processos seletivos. |
| **Infraestrutura como Código (IaC)** | Scripts de automação, Dockerfiles e manifestos Kubernetes são versionados no Git, garantindo rastreabilidade e reversão de mudanças. |
| **CI/CD** | O Git é o gatilho para as pipelines de Integração e Entrega Contínua, automatizando o *build* e *deploy* da aplicação. |

---

## 🛠️ Ambiente de Trabalho

Você utilizará o **VSCode no seu computador** conectado via **Remote SSH na VM Ubuntu**, simulando um ambiente de desenvolvimento e operação profissional.

**Fluxo de Trabalho:**

1.  O VSCode conecta na VM via SSH.
2.  Você edita arquivos remotamente, como se estivessem no seu computador.
3.  O Git e o Docker rodam **dentro da VM**, garantindo um ambiente de testes idêntico ao de produção.

---

## ✅ Pré-requisitos

Certifique-se de que os seguintes itens estão configurados **antes de iniciar o Lab 1**:

### Na sua VM Ubuntu

*   [ ] Ubuntu 24.04 LTS configurado e rodando.
*   [ ] SSH habilitado e acessível.
*   [ ] Git instalado (versão 2.40+).
*   [ ] Python 3.12+ com `pip` funcional.
*   [ ] Conta criada no GitHub.com e SSH keys configuradas.

### No seu computador (Local)

*   [ ] VSCode instalado.
*   [ ] Extensão **Remote SSH** instalada no VSCode.
*   [ ] Git instalado localmente (necessário para o Remote SSH).

### Verificação Rápida na VM

```bash
# Conecte na VM e execute:
git --version
python3 --version
ssh -T git@github.com
```

**Saída esperada do último comando:** `Hi seu-usuario! You've successfully authenticated...`

---

## 📚 Estrutura do Módulo (4 Horas)

O módulo é composto por 4 Labs práticos e progressivos, utilizando o projeto **TaskManager**.

| Lab | Título | Duração | Foco Principal |
| :---: | :--- | :--- | :--- |
| **1** | **Setup e Exploração** | 30 min | Configuração inicial do Git, clonagem do projeto e primeiros `commit`s. |
| **2** | **Configurações DevOps** | 45 min | Versionamento de variáveis de ambiente, *health checks* e *logging* estruturado. |
| **3** | **Branches e Merge** | 45 min | Criação de *feature branches*, desenvolvimento isolado e integração de mudanças via `git merge`. |
| **4** | **GitHub e Pull Request** | 60 min | Fluxo completo de colaboração: **Fork**, configuração de *remotes* e abertura de **Pull Request (PR)**. |

---

## 💻 Setup Prático

### 1. Descobrindo o IP da sua VM

Você precisará do IP para conectar o VSCode e testar a aplicação.

**Na VM Ubuntu, execute:**

```bash
hostname -I
```

**Anote o IP** (ex: `192.168.x.x` ou `10.0.x.x`).

### 2. Conectando via VSCode Remote SSH

1.  Abra a **Command Palette** (`Ctrl + Shift + P`).
2.  Digite: `Remote-SSH: Connect to Host`.
3.  Adicione o host: `devops@<ip-da-vm>`.
4.  Confirme o tipo de SO como **Linux** e digite a senha da VM.

### 3. Testando a Aplicação

Quando rodar o TaskManager na VM, você poderá acessar no navegador do seu computador:

```
http://<ip-da-vm>:5000
```

---

## 📝 O Projeto TaskManager

O TaskManager é um sistema de gerenciamento de tarefas (to-do list) que evoluirá em cada módulo.

| Módulo | Evolução do Projeto |
| :---: | :--- |
| **03** | Versionar e melhorar configurações (Git) |
| **04** | Containerizar com Docker |
| **05** | Orquestração com Docker Compose (Redis + PostgreSQL + Nginx) |
| **06** | Automatizar deploy com Ansible (IaC) |
| **07** | Pipeline CI/CD completo |
| **08** | Observabilidade com Prometheus + Grafana |

**Tecnologias Utilizadas:** Python 3.12 + Flask, Ubuntu 24.04 LTS, Git + GitHub, VSCode Remote SSH.

---

## 💡 Dicas para o Sucesso

### Durante os Labs
*   Leia cada passo com atenção antes de executar.
*   Valide cada *checkpoint* antes de avançar.
*   Entenda o "por quê" de cada comando.
*   Pergunte quando tiver dúvidas.

### Boas Práticas
*   Commits pequenos e frequentes.
*   Mensagens de commit claras e descritivas.
*   Teste antes de commitar.
*   Mantenha histórico limpo.

### Mindset DevOps
*   Automatize tarefas repetitivas.
*   Documente decisões importantes.
*   Versione tudo (código e configuração).
*   Colabore de forma transparente.

---

## ⚠️ Observações Importantes

### Sobre Programação
*   Você não precisa saber programar.
*   O código já vem pronto e funcional.
*   Foco é em práticas DevOps, não desenvolvimento.
*   Edições serão guiadas passo a passo.

### Sobre o Ambiente
*   Tudo será feito remotamente na VM.
*   Não instale Python no seu computador local (use o da VM).
*   Acesse aplicação via IP da VM, não `localhost`.
*   Todos os comandos Git rodam dentro da VM.

### Sobre Erros
*   Errar faz parte do processo.
*   Git permite desfazer mudanças.
*   Instrutor está aqui para ajudar.
*   Dúvidas são bem-vindas.

---

## 🔗 Material de Apoio

*   **`conteudo-git.md`**: Conceitos teóricos de Git.
*   **`labs.md`**: Instruções passo a passo de cada lab.
*   **`troubleshooting.md`**: Soluções para erros comuns.

---

## ⌨️ Atalhos Úteis do VSCode

| Ação | Atalho (Windows/Mac/Linux) |
| :--- | :--- |
| Command Palette | `Ctrl + Shift + P` |
| Abrir/fechar terminal | `Ctrl + J` |
| Buscar arquivos | `Ctrl + P` |
| Salvar arquivo | `Ctrl + S` |
| Buscar em todos arquivos | `Ctrl + Shift + F` |
| Parar processo (Terminal) | `Ctrl + C` |
| Limpar terminal | `Ctrl + L` |

---

## ➡️ Próximo Passo

**Conecte no VSCode via Remote SSH** e abra o arquivo **`lab01-setup.md`** para iniciar o primeiro lab prático.

---

**Versão:** 2.1 (Remote SSH - Multi-platform)  
**Data:** 2025  
**Instrutor:** DevOps Bootcamp Team  
**Suporte:** GitHub Issues do repositório do curso
