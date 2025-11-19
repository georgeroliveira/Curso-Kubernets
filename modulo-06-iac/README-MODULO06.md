# 🧩 Módulo 06 — Infrastructure as Code (IaC)

Neste módulo, você aprenderá como transformar ambientes manuais em ambientes **100% automatizados**, usando Shell Script como camada de IaC.

Você pegará todo o ambiente criado no Módulo 05 (Docker + Docker Compose) e evoluirá para:

- provisionamento automático (dev e prod)
- scripts de manutenção
- automação de health checks
- automação de logs
- automação de atualização
- automação de limpeza
- preparo completo para CI/CD no próximo módulo

---

# 🎯 Objetivos do Módulo

1. Entender o conceito de IaC aplicado no mundo real.  
2. Automatizar o ambiente TaskManager com Shell Script.  
3. Criar scripts de provisionamento para Dev e Prod.  
4. Criar rotinas de monitoramento e manutenção.  
5. Eliminar tarefas manuais.  
6. Preparar o projeto para CI/CD (Módulo 07).  

---

# 📦 Estrutura Final do Módulo

```
modulo-06-iac/
├── labs/
│   ├── lab01_shell_basico.md
│   ├── lab02_iac_ambiente_dev.md
│   ├── lab03_iac_ambiente_prod.md
│   └── lab04_health_logs.md
├── teoria/
│   ├── modulo6_conceitos.md
│   └── modulo6_shell.md
├── projeto-taskmanager/
│   ├── VERSION
│   ├── app.py
│   ├── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx.conf
│   ├── db/
│   ├── static/
│   ├── templates/
│   └── scripts/
│       ├── setup_dev.sh
│       ├── setup_prod.sh
│       ├── health_check.sh
│       ├── logs.sh
│       ├── update_app.sh
│       └── limpar.sh
└── README.md
```

---

# 🛠️ Scripts Criados no Módulo

### ✔ `setup_dev.sh`
Sobe o ambiente de desenvolvimento.

### ✔ `setup_prod.sh`
Sobe o ambiente de produção.

### ✔ `health_check.sh`
Testa a saúde da aplicação.

### ✔ `logs.sh`
Mostra logs ao vivo.

### ✔ `update_app.sh`
Atualiza código e recria containers.

### ✔ `limpar.sh`
Remove containers, volumes e redes.

---

# 🌐 Como subir o ambiente

## 🔹 Ambiente Dev (local)
```
cd projeto-taskmanager
./scripts/setup_dev.sh
```

## 🔹 Ambiente Prod
```
cd projeto-taskmanager
./scripts/setup_prod.sh
```

---

# 🧪 Testes rápidos

### Health
```
./scripts/health_check.sh
```

### Logs
```
./scripts/logs.sh
```

### Atualizar aplicação
```
./scripts/update_app.sh
```

### Reset total
```
./scripts/limpar.sh
```

---

# 📘 Conteúdos do Módulo

### Teoria
- Introdução a IaC
- Automação no DevOps
- Infraestrutura declarativa
- Shell Script aplicado ao pipeline DevOps

### Labs
- Criando scripts
- Provisionando ambiente Dev
- Provisionando Prod
- Criando health/logs/reset/update

---

# 🎯 Conclusão

Você automatizou o projeto TaskManager e eliminou tarefas manuais, deixando tudo reproduzível e pronto para CI/CD.

Próximo módulo:

# 🚀 Módulo 07 — CI/CD com GitHub Actions
