# Git para Iniciantes em DevOps

## Por que aprender Git?

### Sem Git - O Caos
Imagine que você está configurando um servidor e:
- Fez uma mudança que quebrou tudo
- Não lembra o que mudou
- Não tem como voltar atrás
- Perdeu horas de trabalho

### Com Git - Controle Total
- Cada mudança é salva
- Pode voltar versões antigas
- Sabe quem mudou e quando
- Nunca perde trabalho

## Git vs GitHub - Qual a diferença?

### Git
- **O que é:** Programa no seu computador
- **Função:** Controlar versões dos arquivos
- **Onde fica:** Na sua máquina (pasta .git)
- **Funciona:** Sem internet

### GitHub
- **O que é:** Site na internet
- **Função:** Guardar backup e colaborar
- **Onde fica:** Nos servidores do GitHub
- **Funciona:** Precisa internet

**Analogia:** Git é como o Word no seu PC. GitHub é como o Google Drive onde você salva o documento.

## Conceitos Básicos

### 1. Repositório (Repo)
- É a pasta do seu projeto com Git
- Contém todos os arquivos e histórico
- Exemplo: pasta `taskmanager/`

### 2. Commit
- É como tirar uma "foto" do projeto
- Salva o estado atual dos arquivos
- Tem mensagem explicando o que mudou
- Exemplo: "adiciona configuração de logs"

### 3. Branch
- É uma "linha do tempo" alternativa
- Permite fazer mudanças sem afetar o principal
- Útil para testar ideias
- Exemplo: branch "melhorar-logs"

### 4. Main (ou Master)
- Branch principal do projeto
- Código que está funcionando
- De onde saem outras branches

## Comandos Essenciais

### Comandos do Dia a Dia

```bash
# Ver o que mudou
git status

# Adicionar mudanças
git add .

# Salvar mudanças
git commit -m "mensagem explicativa"

# Ver histórico
git log --oneline
```

### Comandos com GitHub

```bash
# Baixar projeto
git clone https://github.com/usuario/projeto

# Enviar mudanças
git push

# Baixar atualizações
git pull
```

## Fluxo de Trabalho DevOps

### 1. Modificar Configurações
- Edita arquivo de config
- Melhora script
- Adiciona monitoramento

### 2. Testar Localmente
- Verifica se funciona
- Corrige erros
- Valida mudanças

### 3. Salvar no Git
```bash
git add .
git commit -m "melhora monitoramento do sistema"
```

### 4. Compartilhar
```bash
git push origin main
```

## Mensagens de Commit

### Boas Mensagens
- "adiciona variáveis de ambiente"
- "corrige porta do health check"  
- "melhora logs do sistema"
- "prepara app para Docker"

### Mensagens Ruins
- "mudanças"
- "fix"
- "teste"
- "asdfasdf"

**Dica:** A mensagem deve explicar O QUE mudou e POR QUE.

## Branches na Prática

### Quando Criar Branch?
- Mudança grande
- Teste de ideia nova
- Correção complexa
- Feature nova

### Exemplo Prático
```bash
# Criar e entrar na branch
git checkout -b melhorar-logs

# Fazer mudanças e commitar
git add .
git commit -m "adiciona logs estruturados"

# Voltar pra main
git checkout main

# Juntar mudanças
git merge melhorar-logs
```

## Erros Comuns e Soluções

### "Esqueci de Configurar Git"
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### "Commitei Errado"
```bash
# Se não fez push ainda
git commit --amend -m "mensagem correta"
```

### "Tá Tudo Bagunçado"
```bash
# Ver o que mudou
git status

# Desfazer mudanças não salvas
git checkout -- arquivo.py
```

## Git para DevOps

### Versionando Configurações
- Scripts de instalação
- Arquivos de config
- Dockerfiles
- Manifestos Kubernetes

### Colaboração em Equipe
- Code review
- Aprovar mudanças
- Documentar decisões
- Rastrear problemas

### Automação
- Git dispara pipelines
- Deploy automático
- Testes ao commitar
- Alertas de mudanças

## Próximos Passos

No módulo, você vai:
1. Configurar Git
2. Versionar o TaskManager
3. Fazer melhorias DevOps
4. Colaborar via GitHub

Lembre-se:
- **Não tenha medo de errar** - Git permite desfazer
- **Commite frequentemente** - Melhor muitos pequenos que um gigante
- **Mensagens claras** - Seu eu do futuro agradece
- **Pratique** - Git se aprende usando

## Resumo

Git é a ferramenta fundamental de todo DevOps porque:
- Versiona infraestrutura como código
- Permite colaboração em equipe
- Mantém histórico de mudanças
- Facilita automação

**Próximo passo:** Vamos para os labs práticos!