# ================================
# Logstash Custom Dockerfile
# ================================

FROM docker.elastic.co/logstash/logstash:8.9.0

LABEL maintainer="Projet Big Data IoT"
LABEL description="Logstash avec pipelines personnalisés pour IoT"

# Variables d'environnement
ENV LS_JAVA_OPTS="-Xmx512m -Xms512m"

# Copier les configurations
COPY config/logstash.yaml /usr/share/logstash/config/logstash.yaml
COPY pipeline/*.conf /usr/share/logstash/pipeline/

# Créer répertoires pour les fichiers d'entrée
RUN mkdir -p /usr/share/logstash/input_files && \
    chown -R logstash:logstash /usr/share/logstash/input_files

# Exposer les ports
EXPOSE 5044 5000 9600

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:9600/_node/stats || exit 1

# Commande par défaut - charger tous les pipelines
CMD ["logstash", "-f", "/usr/share/logstash/pipeline/"]
