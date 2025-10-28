FROM python:3.11-slim

# Metadata
LABEL maintainer="DevOps Course"
LABEL version="1.0"
LABEL description="TaskManager Flask Application"

# Instalar dependencias do sistema
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Criar usuario nao-root
RUN useradd -m -u 1000 appuser

# Criar diretorio da aplicacao
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo da aplicacao
COPY . .

# Criar diretorios para logs e data
RUN mkdir -p /app/logs /app/data && \
    chown -R appuser:appuser /app

# Mudar para usuario nao-root
USER appuser

# Expor porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando para rodar aplicacao
CMD ["python", "app.py"]