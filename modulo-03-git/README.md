# Módulo 03 - Git do Zero ao Pull Request  
Versão 2.1 • DevOps Bootcamp 2025

## O que vamos aprender hoje

Neste módulo você vai aprender a versionar código como um profissional DevOps. Vamos trabalhar com um projeto real (TaskManager) que será usado durante todo o bootcamp.

---

## Ambiente de Trabalho

Você vai usar o **VSCode no seu computador** para editar arquivos que estão **dentro da VM Ubuntu**.

### Como funciona o fluxo
1. VSCode conecta na VM via SSH (Remote SSH)
2. Você edita arquivos remotamente como se estivessem no seu computador
3. Testa a aplicação rodando na VM
4. Commita e faz push direto da VM para o GitHub

### Por que trabalhar assim?
- Simula ambiente real de produção
- Evita diferenças entre Windows/Mac/Linux e ambiente de deploy
- Git configurado uma vez só (na VM)
- Tudo testado no mesmo ambiente que vai rodar em produção
- Aprende workflow profissional desde o início

---

## Pré-requisitos

Antes de começar este módulo, você deve ter:

### Na sua VM Ubuntu
- [ ] Ubuntu 24.04 LTS configurado e rodando
- [ ] SSH habilitado e acessível
- [ ] Git instalado (versão 2.40+)
- [ ] Python 3.12+ com pip funcional
- [ ] Conta criada no GitHub.com
- [ ] SSH keys configuradas no GitHub

### No seu computador (Windows/Mac/Linux)
- [ ] VSCode instalado
- [ ] Extensão Remote SSH instalada no VSCode
- [ ] Git instalado localmente (requerido pelo Remote SSH)
- [ ] Conexão SSH testada: `ssh devops@<ip-da-vm>`

### Verificar versões na VM
```bash
# Conecte na VM e execute:
git --version
python3 --version
ssh -T git@github.com
```

**Saída esperada do último comando:**
```
Hi seu-usuario! You've successfully authenticated...
```

---

## Como vai funcionar a aula

### 1. Conectar no Servidor
- Abrir VSCode e conectar na VM via Remote SSH
- Explorar o ambiente remoto

### 2. Trabalhar com Código Pronto
- Você vai receber o TaskManager já funcional
- Não precisa programar do zero

### 3. Aplicar Melhorias DevOps
- Adicionar configurações profissionais
- Implementar logs e monitoramento
- Preparar para produção

### 4. Versionar com Git
- Fazer commits organizados
- Trabalhar com branches
- Colaborar via GitHub

### 5. Criar Pull Request
- Seu primeiro PR profissional
- Simular workflow de equipe

---

## Por que isso é importante

### No Mercado de Trabalho
- 100% das empresas tech usam Git
- DevOps vive no terminal SSH editando configs remotamente
- GitHub é seu portfólio técnico
- Pull Requests são avaliados em processos seletivos

### Para sua Carreira
- Infraestrutura é versionada como código (IaC)
- Pipelines CI/CD dependem de Git
- Colaboração em equipe exige domínio de branches
- Documentação técnica vive em repositórios

---

## Estrutura da Aula (4 horas)

### Primeira Hora - Setup e Exploração
- Conectar VSCode na VM via Remote SSH
- Configurar Git na VM (user.name e email)
- Clonar primeiro projeto dentro da VM
- Entender estrutura do TaskManager
- Fazer primeiros commits

### Segunda Hora - Configurações DevOps
- Adicionar variáveis de ambiente
- Implementar health checks robustos
- Configurar logging estruturado
- Trabalhar com múltiplos commits organizados

### Terceira Hora - Branches e Colaboração
- Criar branches de feature
- Desenvolver melhorias isoladamente
- Fazer merge de forma profissional
- Entender workflows de equipe

### Quarta Hora - GitHub e Pull Request
- Fazer fork de repositório da turma
- Configurar remotes (origin e upstream)
- Abrir Pull Request real
- Sincronizar repositórios
- Tirar dúvidas e revisão

---

## O Projeto TaskManager

Sistema de gerenciamento de tarefas (to-do list) que evoluirá ao longo do curso.

### Evolução do Projeto
- **Módulo 3 (hoje):** Versionar e melhorar configurações
- **Módulo 4:** Containerizar com Docker
- **Módulo 5:** Adicionar Redis + PostgreSQL + Nginx
- **Módulo 6:** Automatizar deploy com Ansible
- **Módulo 7:** Pipeline CI/CD completo
- **Módulo 8:** Observabilidade com Prometheus + Grafana

### Tecnologias Utilizadas
- **Backend:** Python 3.12 + Flask
- **Ambiente:** Ubuntu 24.04 LTS
- **Versionamento:** Git + GitHub
- **Editor:** VSCode Remote SSH

---

## Observações Importantes

### Sobre Programação
- Você não precisa saber programar
- O código já vem pronto e funcional
- Foco é em práticas DevOps, não desenvolvimento
- Edições serão guiadas passo a passo

### Sobre o Ambiente
- Tudo será feito remotamente na VM
- Não instale Python no seu computador local (use o da VM)
- Acesse aplicação via IP da VM, não localhost
- Todos os comandos Git rodam dentro da VM

### Sobre Erros
- Errar faz parte do processo
- Git permite desfazer mudanças
- Instrutor está aqui para ajudar
- Dúvidas são bem-vindas

---

## Descobrindo o IP da sua VM

Você vai precisar do IP para conectar e testar a aplicação.

### Na VM Ubuntu, execute:
```bash
ip addr show | grep inet
```

**Ou simplesmente:**
```bash
hostname -I
```

**Anote o IP** (algo como `192.168.x.x` ou `10.0.x.x`)

---

## Conectando via VSCode Remote SSH

### Passo 1: Abrir Command Palette
**Atalho:** `Ctrl + Shift + P` (funciona em Windows/Mac/Linux)

Digite: `Remote-SSH: Connect to Host`

### Passo 2: Adicionar Host
```
devops@<ip-da-vm>
```

### Passo 3: Confirmar
- Selecione tipo de SO: **Linux**
- Digite a senha da VM quando solicitado

### Passo 4: Verificar Conexão
- Canto inferior esquerdo do VSCode deve mostrar: `SSH: <ip-da-vm>`
- Terminal integrado já está conectado na VM

---

## Testando a Aplicação

Quando rodar o TaskManager na VM, você poderá acessar no navegador do seu computador:

```
http://<ip-da-vm>:5000
```

**Exemplo:**
```
http://192.168.64.5:5000
```

O VSCode Remote SSH cria túneis automaticamente, mas também pode acessar diretamente via IP da VM.

---

## Estrutura dos Labs

Você vai seguir 4 labs práticos em sequência:

1. **Lab 1 - Setup e Exploração** (30 min)
   - Configurar Git na VM
   - Clonar projeto
   - Primeiro commit

2. **Lab 2 - Configurações DevOps** (45 min)
   - Variáveis de ambiente
   - Health checks
   - Logging profissional

3. **Lab 3 - Branches** (45 min)
   - Criar feature branch
   - Merge sem conflitos
   - Fluxo de desenvolvimento

4. **Lab 4 - GitHub e PR** (60 min)
   - Fork de repositório
   - Pull Request
   - Code review

---

## Material de Apoio

Durante a aula, você terá acesso a:

- **conteudo-git.md:** Conceitos teóricos de Git
- **labs.md:** Instruções passo a passo de cada lab
- **troubleshooting.md:** Soluções para erros comuns

Todos os arquivos estarão disponíveis no repositório do curso.

---

## Checklist Final

Antes de iniciar o Lab 1, confirme:

- [ ] VSCode conectado na VM via Remote SSH
- [ ] Terminal do VSCode mostra prompt da VM Ubuntu
- [ ] Consegue executar `git --version` no terminal integrado
- [ ] IP da VM anotado e acessível
- [ ] GitHub configurado com SSH keys
- [ ] Pasta de trabalho criada: `~/devops-bootcamp`

---

## Próximo Passo

**Conecte no VSCode via Remote SSH** e abra o arquivo **`lab01-setup.md`** para iniciar o primeiro lab prático.

Lembre-se: você está trabalhando remotamente na VM, não no seu computador local.

---

## Dicas para o Sucesso

### Durante os Labs
- Leia cada passo com atenção antes de executar
- Valide cada checkpoint antes de avançar
- Entenda o "por quê" de cada comando
- Pergunte quando tiver dúvidas

### Boas Práticas
- Commits pequenos e frequentes
- Mensagens de commit claras e descritivas
- Teste antes de commitar
- Mantenha histórico limpo

### Mindset DevOps
- Automatize tarefas repetitivas
- Documente decisões importantes
- Versione tudo (código e configuração)
- Colabore de forma transparente

---

## Atalhos Úteis do VSCode

**Gerais (Windows/Mac/Linux):**
- `Ctrl + Shift + P` - Command Palette
- `Ctrl + J` - Abrir/fechar terminal
- `Ctrl + P` - Buscar arquivos
- `Ctrl + S` - Salvar arquivo
- `Ctrl + Shift + F` - Buscar em todos arquivos

**Terminal:**
- `Ctrl + C` - Parar processo
- `Ctrl + L` - Limpar terminal
- Setas cima/baixo - Navegar histórico de comandos

---

**Versão:** 2.1 (Remote SSH - Multi-platform)  
**Data:** 2025  
**Instrutor:** DevOps Bootcamp Team  
**Suporte:** GitHub Issues do repositório do curso