# Usar imagem especifica e menor
FROM python:3.11-slim

# Metadados
LABEL maintainer="DevOps Bootcamp"
LABEL version="1.0"
LABEL description="TaskManager containerizado"

# Variaveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production

# Criar usuario nao-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar dependencias do sistema (se necessario)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Diretorio de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache de layers)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar codigo da aplicacao
COPY --chown=appuser:appuser . .

# Criar diretorio para dados
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Trocar para usuario nao-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expor porta
EXPOSE 5000

# Comando para executar
CMD ["python", "app.py"]