# 🏢 Plateforme IoT Big Data - Système de Gestion Intelligente de Bâtiments

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Angular](https://img.shields.io/badge/Angular-17-red.svg)](https://angular.io/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.9-yellow.svg)](https://www.elastic.co/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

Plateforme complète de gestion et d'analyse de données IoT pour le monitoring de bâtiments intelligents. Le système collecte, traite et analyse en temps réel les données provenant de capteurs, alertes, consommation énergétique, occupation des salles et maintenance des équipements.

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Fonctionnalités](#-fonctionnalités)
- [Installation Rapide](#-installation-rapide)
- [Guide d'utilisation](#-guide-dutilisation)
- [API Documentation](#-api-documentation)
- [Structure du Projet](#-structure-du-projet)
- [Tests](#-tests)
- [Dépannage](#-dépannage)
- [Contribution](#-contribution)

---

## 🎯 Vue d'ensemble

Ce projet est une plateforme Big Data complète permettant de :
- **Collecter** des données IoT depuis multiples sources (JSON, CSV, NDJSON)
- **Traiter** les données en temps réel via un pipeline Logstash
- **Stocker** dans Elasticsearch pour une recherche ultra-rapide
- **Analyser** avec des API REST Django performantes
- **Visualiser** via une interface Angular moderne et Kibana

### Cas d'usage principaux

1. **Monitoring en temps réel** : Surveillance continue de 5 types de données IoT
2. **Alertes intelligentes** : Détection et classification automatique des anomalies
3. **Analyse prédictive** : Maintenance préventive basée sur l'historique
4. **Optimisation énergétique** : Suivi et réduction de la consommation
5. **Gestion d'espace** : Optimisation de l'occupation des salles

---

## 🏗️ Architecture

### Architecture Globale

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PLATEFORME IOT BIG DATA                         │
└─────────────────────────────────────────────────────────────────────────┘

 ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌──────────┐
 │  Fichiers   │────▶│   Django    │────▶│    Redis    │────▶│ Logstash │
 │   Logs      │     │ Upload API  │     │   Queue     │     │ Pipeline │
 │ (CSV/JSON)  │     │             │     │             │     │          │
 └─────────────┘     └─────────────┘     └─────────────┘     └─────┬────┘
                                                                     │
                                                                     ▼
 ┌─────────────┐     ┌─────────────┐     ┌────────────────────────────┐
 │   Angular   │◀────│   Django    │◀────│     Elasticsearch          │
 │  Frontend   │     │  REST API   │     │   (5 indices IoT)          │
 │             │     │             │     │  - iot-alertes             │
 └──────┬──────┘     └─────────────┘     │  - iot-capteurs            │
        │                   ▲             │  - iot-consommation        │
        │                   │             │  - iot-occupation          │
        ▼                   │             │  - iot-maintenance         │
 ┌─────────────┐     ┌──────────────┐    └────────────────────────────┘
 │   Kibana    │────▶│ Elasticsearch│                 ▲
 │ Dashboards  │     │              │                 │
 └─────────────┘     └──────────────┘     ┌───────────┴────────────┐
                                           │   Recherche temps réel │
                                           │   Agrégations          │
                                           │   Analytics            │
                                           └────────────────────────┘
```

### Flux de données détaillé

1. **Ingestion** : Upload de fichiers (CSV/JSON) via API Django ou interface Angular
2. **Mise en queue** : Stockage temporaire dans Redis pour traitement asynchrone
3. **Transformation** : Logstash lit Redis, parse et enrichit les données
4. **Indexation** : Elasticsearch indexe les données pour recherche rapide
5. **Exposition** : Django REST API expose les données
6. **Visualisation** : Angular + Kibana affichent les résultats

---

## 🛠️ Technologies

### Stack Backend

| Technologie | Version | Rôle |
|------------|---------|------|
| **Python** | 3.11 | Langage principal |
| **Django** | 5.0 | Framework web |
| **Django REST Framework** | 3.14 | API RESTful |
| **Elasticsearch** | 8.9.0 | Moteur de recherche & analytics |
| **Logstash** | 8.9.0 | Pipeline ETL temps réel |
| **Redis** | 7.0 | Cache & file de messages |
| **Kibana** | 8.9.0 | Visualisation de données |

### Stack Frontend

| Technologie | Version | Rôle |
|------------|---------|------|
| **Angular** | 17 | Framework SPA |
| **TypeScript** | 5.2 | Typage statique |
| **RxJS** | 7.8 | Programmation réactive |
| **SCSS** | - | Stylisation |

### DevOps & Infrastructure

| Technologie | Rôle |
|------------|------|
| **Docker** | Containerisation |
| **Docker Compose** | Orchestration multi-conteneurs |
| **Git** | Contrôle de version |

---

## ✨ Fonctionnalités

### 🚨 1. Gestion des Alertes
- **Monitoring temps réel** des alertes de capteurs IoT
- **Classification automatique** par sévérité (critique, haute, moyenne, faible)
- **Suivi du statut** (non résolue, en cours, résolue, fermée)
- **Statistiques avancées** : agrégations par catégorie, bâtiment, sévérité, zone
- **Recherche full-text** avec filtres multiples
- **API REST complète** avec pagination

### 📡 2. Données des Capteurs
- **Collecte multi-capteurs** : température, humidité, CO2, luminosité, mouvement
- **Monitoring d'état** : actif, inactif, maintenance, défaillant
- **Suivi batterie** : alertes niveau faible
- **Historique calibrations** : traçabilité complète
- **Analyse de dérives** : détection d'anomalies
- **Géolocalisation** : position par bâtiment/zone/étage

### ⚡ 3. Consommation Énergétique
- **Multi-énergies** : électricité, eau, gaz
- **Typologie détaillée** : climatisation, éclairage, chauffage, équipements
- **Calcul coûts** : estimation en euros
- **Empreinte carbone** : CO2 équivalent en kg
- **Comparaisons temporelles** : jour/semaine/mois
- **Détection surconsommation** : alertes automatiques

### 👥 4. Occupation des Salles
- **Temps réel** : monitoring instantané
- **Réservations** : gestion complète des événements
- **Taux d'utilisation** : statistiques d'occupation
- **Équipements** : suivi des ressources utilisées
- **Capacité vs utilisation** : optimisation de l'espace
- **Prédictions** : analyse des tendances

### 🔧 5. Maintenance Préventive
- **Planification** : interventions programmées
- **Prédiction pannes** : ML sur historique
- **Durée de vie** : suivi équipements
- **Coûts maintenance** : budget et prévisions
- **Prioritisation** : par criticité
- **Historique complet** : traçabilité interventions

### 🔍 6. Recherche Elasticsearch
- **Full-text search** sur tous les champs
- **Recherche floue** : tolérance aux fautes
- **Filtres multiples** : combinaison de critères
- **Agrégations** : statistiques en temps réel
- **Tri dynamique** : par score, date, valeur
- **Pagination** : navigation efficace

### 📊 7. Interface Angular Moderne
- **Upload drag & drop** : fichiers CSV/JSON
- **Détection automatique** du type de données
- **Dashboard interactif** : statistiques en temps réel
- **Recherche avancée** : interface intuitive
- **Top 3 résultats** : mise en évidence (🥇🥈🥉)
- **Refresh automatique** : après upload
- **Kibana intégré** : iframe sécurisée

---

## 📦 Prérequis

### Logiciels requis

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**
- **Node.js 18+** et **npm** (optionnel, pour dev Angular local)
- **Python 3.11+** (optionnel, pour dev Django local)

### Ressources système recommandées

- **RAM** : 8 GB minimum (16 GB recommandé)
- **CPU** : 4 cœurs minimum
- **Disque** : 10 GB d'espace libre
- **Réseau** : Connexion internet (première installation)
- **Python 3.11+** (pour le développement Django)

### Ports requis
- 8000 - Django API
- 4200 - Angular Dev Server
- 9200 - Elasticsearch
- 5601 - Kibana
- 6379 - Redis
- 5044 - Logstash

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone <repository-url>
cd Projet
```

### 2. Démarrer les services Docker

```bash
docker-compose up -d
```

Cette commande démarre tous les services :
- Elasticsearch
- Kibana
- Logstash
- Redis
- Django API

### 3. Vérifier que tous les services sont actifs

```bash
docker-compose ps
```

Tous les services doivent être dans l'état "Up".

### 4. Accéder aux interfaces

- **Django API**: http://localhost:8000/api/
- **Kibana**: http://localhost:5601
- **Elasticsearch**: http://localhost:9200

## ⚙️ Configuration

### Fichiers de logs

Les fichiers de logs sources sont dans le répertoire `Fichier_logs/` :
- `logs_alertes.json` - Alertes des capteurs (JSON)
- `logs_capteurs.csv` - Données des capteurs (CSV)
- `logs_consommation.json` - Consommation énergétique (JSON)
- `logs_occupation.csv` - Occupation des salles (CSV)
- `logs_maintenance.csv` - Interventions de maintenance (CSV)

### Pipelines Logstash

5 pipelines configurés dans `logstash/pipeline/` :
- `alertes-to-elasticsearch.conf`
- `capteurs-to-elasticsearch.conf`
- `consommation-to-elasticsearch.conf`
- `occupation-to-elasticsearch.conf`
- `file-to-elasticsearch.conf` (maintenance)

### Variables d'environnement

Les variables principales sont configurées dans `docker-compose.yaml` :
- `ELASTICSEARCH_HOST=elasticsearch:9200`
- `REDIS_HOST=redis`
- `REDIS_PORT=6379`

## 📖 Utilisation

### Vérifier l'ingestion des données

```bash
# Vérifier les indices Elasticsearch
curl http://localhost:9200/_cat/indices?v

# Compter les documents dans chaque index
curl http://localhost:9200/iot-alertes/_count
curl http://localhost:9200/iot-capteurs/_count
curl http://localhost:9200/iot-consommation/_count
curl http://localhost:9200/iot-occupation/_count
curl http://localhost:9200/iot-maintenance/_count
```

### Tester l'API Django

```bash
# Health check
curl http://localhost:8000/api/health

# Récupérer les alertes
curl http://localhost:8000/api/alertes?size=10

# Obtenir les statistiques
curl http://localhost:8000/api/alertes/stats
```

### Développement Angular

```bash
cd angular-app
npm install
npm start
```

L'application sera accessible sur http://localhost:4200

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### Alertes
```
GET /api/alertes              # Liste des alertes
GET /api/alertes/stats        # Statistiques
Paramètres: q, size, from, severite, statut, categorie, batiment, sort_by, sort_order
```

### Capteurs
```
GET /api/capteurs             # Liste des capteurs
GET /api/capteurs/stats       # Statistiques
Paramètres: q, size, from, type, statut, batiment, zone, sort_by, sort_order
```

### Consommation
```
GET /api/consommation         # Données de consommation
GET /api/consommation/stats   # Statistiques
Paramètres: q, size, from, type_energie, sous_type, batiment, zone, sort_by, sort_order
```

### Occupation
```
GET /api/occupation           # Données d'occupation
GET /api/occupation/stats     # Statistiques
Paramètres: q, size, from, type_salle, statut, batiment, zone, sort_by, sort_order
```

### Maintenance
```
GET /api/maintenance          # Données de maintenance
GET /api/maintenance/stats    # Statistiques
Paramètres: q, size, from, type_equipement, type_maintenance, severite, batiment, sort_by, sort_order
```

**Format de réponse standard:**
```json
{
  "total": 100,
  "count": 10,
  "documents": [...],
  "from": 0,
  "size": 10
}
```

Pour plus de détails, consultez le fichier [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md).

## 📁 Structure du Projet

```
Projet/
├── django_app/                 # Backend Django
│   ├── api/                   # Application API
│   │   ├── views.py          # 10 vues API (alertes, capteurs, etc.)
│   │   ├── elasticsearch_service.py  # Service Elasticsearch
│   │   └── serializers.py    # Sérialiseurs Django REST
│   ├── config/               # Configuration Django
│   │   ├── settings.py
│   │   └── urls.py          # Routage URL
│   ├── requirements.txt      # Dépendances Python
│   └── Dockerfile
│
├── angular-app/              # Frontend Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/  # Composants UI
│   │   │   ├── services/    # 5 services HTTP
│   │   │   │   ├── alertes.service.ts
│   │   │   │   ├── capteurs-data.service.ts
│   │   │   │   ├── consommation.service.ts
│   │   │   │   ├── occupation.service.ts
│   │   │   │   └── maintenance-data.service.ts
│   │   │   └── models/      # Interfaces TypeScript
│   │   └── environments/
│   ├── package.json
│   └── angular.json
│
├── logstash/                 # Configuration Logstash
│   ├── pipeline/            # 5 pipelines de traitement
│   │   ├── alertes-to-elasticsearch.conf
│   │   ├── capteurs-to-elasticsearch.conf
│   │   ├── consommation-to-elasticsearch.conf
│   │   ├── occupation-to-elasticsearch.conf
│   │   └── file-to-elasticsearch.conf
│   ├── config/
│   │   └── logstash.yaml
│   └── scripts/             # Scripts utilitaires
│
├── Fichier_logs/            # Fichiers de logs sources
│   ├── logs_alertes.json
│   ├── logs_alertes.ndjson
│   ├── logs_capteurs.csv
│   ├── logs_consommation.json
│   ├── logs_consommation.ndjson
│   ├── logs_occupation.csv
│   └── logs_maintenance.csv
│
├── redis/                   # Configuration Redis
│   ├── redis.conf
│   └── test_redis.py
│
├── docker-compose.yaml      # Orchestration Docker
├── Postman_Collection.json  # Collection Postman
├── API_TESTING_GUIDE.md     # Guide de test des API
└── README.md               # Ce fichier
```

## 🧪 Tests

### Tests avec Postman

1. Importer la collection `Postman_Collection.json`
2. Exécuter les requêtes organisées par catégorie
3. Vérifier les réponses et statistiques

### Tests avec curl

Consulter le fichier [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) pour tous les exemples de requêtes curl.

### Tests unitaires Django

```bash
docker exec -it django_container python manage.py test
```

## 🔧 Dépannage

### Les services ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs -f

# Redémarrer tous les services
docker-compose restart

# Reconstruire les images
docker-compose up -d --build
```

### Elasticsearch ne contient pas de données

```bash
# Vérifier que Logstash traite les fichiers
docker logs logstash_container --tail 100

# Redémarrer Logstash pour réingérer
docker restart logstash_container

# Attendre 30-40 secondes puis vérifier
curl http://localhost:9200/_cat/indices?v
```

### L'API Django ne répond pas

```bash
# Vérifier les logs Django
docker logs django_container --tail 50

# Redémarrer Django
docker restart django_container

# Tester la connexion
curl http://localhost:8000/api/health
```

### Erreurs de connexion Elasticsearch

```bash
# Vérifier qu'Elasticsearch est accessible
curl http://localhost:9200

# Vérifier la configuration dans Django
docker exec django_container env | grep ELASTICSEARCH
```

### Réinitialiser complètement le système

```bash
# Arrêter tous les services
docker-compose down

# Supprimer les volumes (ATTENTION: supprime toutes les données)
docker-compose down -v

# Redémarrer
docker-compose up -d
```

## 📊 Monitoring et Visualisation

### Kibana

Accédez à Kibana sur http://localhost:5601 pour :
- Créer des dashboards personnalisés
- Visualiser les données en temps réel
- Créer des alertes basées sur des seuils
- Analyser les tendances

### Index Patterns

Créer les index patterns dans Kibana :
- `iot-alertes*`
- `iot-capteurs*`
- `iot-consommation*`
- `iot-occupation*`
- `iot-maintenance*`



## 📝 License

Ce projet est développé dans le cadre d'un projet académique Big Data.

## 👥 Auteurs

Projet Big Data - Système de Gestion IoT

## 🙏 Remerciements

- Elastic Stack (Elasticsearch, Logstash, Kibana)
- Django & Django REST Framework
- Angular Framework
- Docker Community



**Note**: Ce projet nécessite Docker et Docker Compose pour fonctionner. Assurez-vous que tous les ports nécessaires sont disponibles avant de démarrer les services.
