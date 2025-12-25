# ========================================
# Guide de Déploiement Kubernetes
# ========================================

## 📋 Prérequis

- Cluster Kubernetes (v1.24+)
- kubectl configuré
- Docker registry (Docker Hub, GCR, ou privé)
- Nginx Ingress Controller installé
- (Optionnel) cert-manager pour HTTPS

## 🏗️ Architecture Kubernetes

```
                          ┌─────────────────┐
                          │     Ingress     │
                          │  (Nginx/TLS)    │
                          └────────┬────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
           ┌──────▼──────┐  ┌─────▼─────┐   ┌─────▼──────┐
           │   Angular   │  │   Django  │   │   Kibana   │
           │ (2 replicas)│  │(3 replicas)│   │(1 replica) │
           └──────┬──────┘  └─────┬─────┘   └─────┬──────┘
                  │                │                │
                  │         ┌──────▼──────┐         │
                  │         │ Logstash    │         │
                  │         │(1 replica)  │         │
                  │         └──────┬──────┘         │
                  │                │                │
                  │         ┌──────▼────────────────▼─────┐
                  │         │      Elasticsearch          │
                  │         │       (StatefulSet)         │
                  │         └──────┬──────────────────────┘
                  │                │
                  └────────────────▼────────────────────────┐
                                   │         Redis          │
                                   │      (StatefulSet)     │
                                   └────────────────────────┘
```

## 🚀 Étape 1 : Build et Push des Images Docker

### 1.1 Se connecter au registry

```bash
# Docker Hub
docker login

# Google Container Registry
gcloud auth configure-docker

# Azure Container Registry
az acr login --name <registry-name>

# AWS ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
```

### 1.2 Build et push Django API

```bash
cd django_app

# Build pour production avec Gunicorn
docker build -f Dockerfile.prod -t <YOUR_REGISTRY>/django-api:latest .
docker push <YOUR_REGISTRY>/django-api:latest

# Ou avec tag de version
docker build -f Dockerfile.prod -t <YOUR_REGISTRY>/django-api:v1.0.0 .
docker push <YOUR_REGISTRY>/django-api:v1.0.0
```

### 1.3 Build et push Angular Frontend

```bash
cd angular-app

docker build -t <YOUR_REGISTRY>/angular-frontend:latest .
docker push <YOUR_REGISTRY>/angular-frontend:latest
```

### 1.4 Build et push Logstash

```bash
cd logstash

docker build -t <YOUR_REGISTRY>/logstash-iot:latest .
docker push <YOUR_REGISTRY>/logstash-iot:latest
```

## 🔧 Étape 2 : Configurer les Manifests Kubernetes

### 2.1 Mettre à jour les images dans les manifests

Remplacez `<YOUR_REGISTRY>` dans tous les fichiers YAML :

```bash
# Avec sed (Linux/Mac)
sed -i 's/<YOUR_REGISTRY>/your-dockerhub-username/g' k8s/*.yaml

# Avec PowerShell (Windows)
Get-ChildItem k8s/*.yaml | ForEach-Object {
    (Get-Content $_) -replace '<YOUR_REGISTRY>', 'your-dockerhub-username' | Set-Content $_
}
```

### 2.2 Mettre à jour les domaines

Remplacez `example.com` par votre domaine :

```bash
# Linux/Mac
sed -i 's/iot-platform.example.com/your-domain.com/g' k8s/*.yaml
sed -i 's/api.iot-platform.example.com/api.your-domain.com/g' k8s/*.yaml

# PowerShell
Get-ChildItem k8s/*.yaml | ForEach-Object {
    (Get-Content $_) -replace 'iot-platform.example.com', 'your-domain.com' | Set-Content $_
}
```

## 🚀 Étape 3 : Déploiement sur Kubernetes

### 3.1 Créer le namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 3.2 Déployer les services dans l'ordre

```bash
# 1. Redis (dépendance de base)
kubectl apply -f k8s/redis.yaml

# 2. Elasticsearch (stockage de données)
kubectl apply -f k8s/elasticsearch.yaml

# 3. Attendre qu'Elasticsearch soit prêt
kubectl wait --for=condition=ready pod -l app=elasticsearch -n iot-platform --timeout=300s

# 4. Kibana (visualisation)
kubectl apply -f k8s/kibana.yaml

# 5. Logstash (pipeline)
kubectl apply -f k8s/logstash.yaml

# 6. Django API (backend)
kubectl apply -f k8s/django.yaml

# 7. Angular Frontend
kubectl apply -f k8s/angular.yaml

# 8. Horizontal Pod Autoscaler
kubectl apply -f k8s/hpa.yaml
```

### 3.3 Déploiement complet en une commande

```bash
kubectl apply -f k8s/ --recursive
```

## 🔍 Étape 4 : Vérification du Déploiement

### 4.1 Vérifier les pods

```bash
# Tous les pods dans le namespace
kubectl get pods -n iot-platform

# Avec surveillance en temps réel
kubectl get pods -n iot-platform -w

# Status détaillé
kubectl describe pods -n iot-platform
```

### 4.2 Vérifier les services

```bash
kubectl get services -n iot-platform
kubectl get ingress -n iot-platform
```

### 4.3 Vérifier les logs

```bash
# Django
kubectl logs -f deployment/django -n iot-platform

# Angular
kubectl logs -f deployment/angular -n iot-platform

# Elasticsearch
kubectl logs -f deployment/elasticsearch -n iot-platform

# Logstash
kubectl logs -f deployment/logstash -n iot-platform
```

### 4.4 Vérifier les health checks

```bash
# Django API
kubectl exec -it deployment/django -n iot-platform -- curl http://localhost:8000/api/health/

# Elasticsearch
kubectl exec -it deployment/elasticsearch -n iot-platform -- curl http://localhost:9200/_cluster/health
```

## 🔐 Étape 5 : Configuration HTTPS (Optionnel)

### 5.1 Installer cert-manager

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

### 5.2 Créer un ClusterIssuer

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

## 📊 Étape 6 : Monitoring et Scaling

### 6.1 Surveiller les ressources

```bash
# CPU et mémoire
kubectl top pods -n iot-platform
kubectl top nodes

# HPA status
kubectl get hpa -n iot-platform
```

### 6.2 Scaling manuel

```bash
# Scale Django
kubectl scale deployment django --replicas=5 -n iot-platform

# Scale Angular
kubectl scale deployment angular --replicas=3 -n iot-platform
```

### 6.3 Voir les événements

```bash
kubectl get events -n iot-platform --sort-by='.lastTimestamp'
```

## 🔄 Étape 7 : Mises à jour

### 7.1 Rolling update

```bash
# Build nouvelle version
docker build -f Dockerfile.prod -t <YOUR_REGISTRY>/django-api:v1.0.1 django_app/
docker push <YOUR_REGISTRY>/django-api:v1.0.1

# Update deployment
kubectl set image deployment/django django=<YOUR_REGISTRY>/django-api:v1.0.1 -n iot-platform

# Surveiller le rollout
kubectl rollout status deployment/django -n iot-platform
```

### 7.2 Rollback

```bash
# Voir l'historique
kubectl rollout history deployment/django -n iot-platform

# Rollback à la version précédente
kubectl rollout undo deployment/django -n iot-platform

# Rollback à une version spécifique
kubectl rollout undo deployment/django --to-revision=2 -n iot-platform
```

## 🧹 Étape 8 : Nettoyage

```bash
# Supprimer tous les ressources
kubectl delete namespace iot-platform

# Ou supprimer individuellement
kubectl delete -f k8s/ --recursive
```

## 🔧 Dépannage

### Pod ne démarre pas

```bash
kubectl describe pod <pod-name> -n iot-platform
kubectl logs <pod-name> -n iot-platform --previous
```

### Service inaccessible

```bash
kubectl get endpoints -n iot-platform
kubectl port-forward svc/django 8000:8000 -n iot-platform
```

### Problèmes de stockage

```bash
kubectl get pv
kubectl get pvc -n iot-platform
kubectl describe pvc <pvc-name> -n iot-platform
```

## 📝 Notes importantes

1. **Ressources** : Ajustez les requests/limits selon votre cluster
2. **Stockage** : Utilisez StorageClass approprié pour votre cloud provider
3. **Secrets** : Utilisez Kubernetes Secrets ou un vault externe
4. **Backup** : Configurez des backups pour Elasticsearch et Redis
5. **Monitoring** : Installez Prometheus + Grafana pour monitoring avancé

## 🎯 Production Checklist

- [ ] Images Docker buildées et pushées
- [ ] Secrets configurés (Redis password, API keys...)
- [ ] PersistentVolumes configurés et provisionés
- [ ] Ingress configuré avec domaine
- [ ] HTTPS activé avec cert-manager
- [ ] HPA configuré et testé
- [ ] Monitoring installé (Prometheus/Grafana)
- [ ] Logs centralisés (ELK, Loki...)
- [ ] Backups configurés
- [ ] CI/CD pipeline configuré
- [ ] Documentation à jour
