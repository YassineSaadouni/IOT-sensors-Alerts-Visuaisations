# ================================
# Django API Backend Dockerfile
# ================================

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Projet Big Data IoT"
LABEL description="Django REST API pour plateforme IoT"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Créer répertoire de travail
WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Créer répertoire pour les médias et les logs
RUN mkdir -p /app/media /app/logs && \
    chmod -R 755 /app/media /app/logs

# Collecter les fichiers statiques (si nécessaire)
# RUN python manage.py collectstatic --noinput

# Exposer le port
EXPOSE 8000

# Créer un utilisateur non-root
RUN useradd -m -u 1000 django && \
    chown -R django:django /app
USER django

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health/', timeout=5)"

# Commande par défaut
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
