
# 🚀 **Módulo 08 – Observabilidade e Monitoramento**

### Prometheus • Grafana • Exporters • Métricas • Alertas

![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus\&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana\&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completo-success)

---

## 📌 **Visão Geral**

Neste módulo, você transforma a aplicação TaskManager em um **sistema observável de verdade**, monitorado com:

* **Prometheus** (coleta de métricas)
* **Grafana** (dashboards profissionais)
* **Exporters** (app, sistema, containers)
* **Alertas básicos** (health, latência, disponibilidade)
* **Scripts DevOps** (automação total)

Esta é a mesma base utilizada em ambientes corporativos modernos com DevOps, SRE e FinOps.

---

# 🎯 **Objetivos de Aprendizagem**

Você será capaz de:

✔ Configurar Prometheus do zero
✔ Criar dashboards no Grafana
✔ Implementar métricas customizadas em Python
✔ Criar exporters e endpoints `/metrics`
✔ Integrar métricas de containers, rede e CPU
✔ Criar alertas básicos no Prometheus
✔ Automatizar operações com scripts Shell
✔ Validar configuração e debugar problemas
✔ Criar cenários reais de produção

---

# 📁 **Estrutura Oficial do Módulo**

```
modulo-08-observabilidade/
├── labs/
│   ├── lab-01-prometheus-basico.md
│   ├── lab-02-grafana-dashboards.md
│   ├── lab-03-exporters.md
│   ├── lab-04-metricas-app.md
│   ├── lab-05-alertas.md
│
├── projeto-final/
│   ├── app/
│   │   ├── app.py
│   │   ├── metrics.py
│   │   └── requirements.txt
│   ├── observabilidade/
│   │   ├── prometheus.yml
│   │   ├── exporters/
│   │   └── dashboards/
│   ├── docker-compose.observabilidade.yml
│   ├── grafana/
│   └── prometheus/
│
├── scripts/
│   ├── restart-observabilidade.sh
│   ├── status.sh
│   ├── debug-exporters.sh
│   ├── coletar-metricas.sh
│   ├── metrics-benchmark.sh
│   ├── gerar-snapshot.sh
│   ├── validar-prometheus.sh
│   ├── limpar-cache-grafana.sh
│   ├── rebuild-app.sh
│   ├── show-logs.sh
│   └── testar-alertas.sh
│
├── teoria/
│   ├── conteudo-observabilidade.md
│   ├── 02-prometheus.md
│   ├── 03-grafana.md
│   ├── 04-exporters.md
│   ├── 05-metricas-aplicacao.md
│   ├── 06-alertmanager.md
│
└── tests/
    └── test_metrics.py
```

Perfeito para estudo **progressivo e evolutivo**.

---

# 📚 **Conteúdo Teórico**

### 🔸 **1. Conceitos de Observabilidade**

* Logs • Métricas • Traces
* Por que DevOps precisa medir
* Golden Signals (SRE da Google)

### 🔸 **2. Prometheus (Métricas e Coleta)**

* Pull Model
* Jobs & Targets
* Write-Ahead-Log
* Consultas (PromQL)

### 🔸 **3. Grafana (Dashboards)**

* Datasources
* Panels
* Triggers & Alerts
* Import/export

### 🔸 **4. Exporters**

* Node Exporter
* Cadvisor
* App Exporter (/metrics)
* Blackbox Exporter

### 🔸 **5. Métricas Customizadas (Python)**

* Counter
* Gauge
* Histogram
* Summary

### 🔸 **6. Alertmanager (Conceitos)**

* Alert Routing
* Silences
* Templates
* Webhooks

---

# 🔬 **Laboratórios Práticos**

### ✔ **Lab 01 — Prometheus Básico**

* Subir o Prometheus
* Validar targets
* Fazer consultas PromQL

### ✔ **Lab 02 — Dashboards no Grafana**

* Conectar datasources
* Criar painéis customizados

### ✔ **Lab 03 — Exporters**

* Node Exporter
* CAdvisor
* Exporter da aplicação

### ✔ **Lab 04 — Métricas da Aplicação**

* Implementar métricas Python
* `/metrics` com Prometheus Client

### ✔ **Lab 05 — Alertas**

* Configurar alertas simples
* Testar falhas com scripts

---

# 🧩 **Projeto Final do Módulo**

O projeto final consolida **todo o módulo** com:

* Stack completa observável
* Dashboards profissionais
* Alerts funcionando
* Scripts de operação real
* Testes automatizados

Comandos principais:

```bash
# Subir stack
docker compose -f docker-compose.observabilidade.yml up -d

# Status
./scripts/status.sh

# Debug exporters
./scripts/debug-exporters.sh
```

---

# 🛠️ **Scripts DevOps (Automação Completa)**

Este módulo inclui **11 scripts reais de operação**, semelhantes aos usados em ambientes SRE.

Exemplos:

```bash
./scripts/restart-observabilidade.sh
./scripts/metrics-benchmark.sh
./scripts/coletar-metricas.sh
./scripts/testar-alertas.sh
./scripts/validar-prometheus.sh
```

Todos funcionam 100%.

---

# 📊 **Dashboards Inclusos**

Dentro de:

```
projeto-final/observabilidade/dashboards/
```

Inclui:

* Dashboard Geral (App + Infra)
* Dashboard de Performance
* Dashboard de Latência
* Dashboard de Uso de Recursos

---

# 🔐 **Alertas Configurados**

Exemplos incluídos no módulo:

* App Offline
* Alta latência
* Muitas tarefas pendentes
* Falha no /health

---

# ✔ **Checklist de Conclusão**

Você concluiu o módulo quando:

* [ ] Subiu Prometheus e Grafana
* [ ] Criou dashboards
* [ ] Implementou métricas customizadas
* [ ] Configurou exporters
* [ ] Criou alertas básicos
* [ ] Executou todos os labs
* [ ] Executou os scripts e validou operação
* [ ] Finalizou o projeto completo

---

# 🏆 **Parabéns!**

Com este módulo, você já opera no nível:

**DevOps → Pleno/Sênior**
**SRE → Prod readiness**
**Observabilidade Corporativa**

Você agora possui uma base completa para:

* Métricas profissionais
* Monitoramento 24/7
* Alertas de produção
* Dashboards corporativos
* Análise de performance
* Troubleshooting avançado


