# Système de Gestion IoT - Big Data Project

Plateforme complète de gestion et d'analyse de données IoT pour le monitoring de bâtiments intelligents. Le système collecte, traite et analyse en temps réel les données provenant de capteurs, alertes, consommation énergétique, occupation des salles et maintenance des équipements.

## 📋 Table des matières

- [Architecture](#architecture)
- [Technologies](#technologies)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [API Endpoints](#api-endpoints)
- [Structure du Projet](#structure-du-projet)
- [Tests](#tests)
- [Dépannage](#dépannage)

## 🏗️ Architecture

Le système est basé sur une architecture microservices containerisée :

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│  Fichiers   │─────▶│   Logstash   │─────▶│Elasticsearch │
│    Logs     │      │  (Pipeline)  │      │  (Storage)   │
└─────────────┘      └──────────────┘      └──────────────┘
                            │                       │
                            │                       ▼
                            │              ┌──────────────┐
                            │              │    Django    │
                            │              │  (REST API)  │
                            │              └──────────────┘
                            │                       │
                            ▼                       ▼
                     ┌──────────┐          ┌──────────────┐
                     │  Redis   │          │   Angular    │
                     │ (Cache)  │          │  (Frontend)  │
                     └──────────┘          └──────────────┘
```

## 🛠️ Technologies

### Backend
- **Python 3.11** - Langage principal
- **Django 5.0** - Framework web
- **Django REST Framework** - API RESTful
- **Elasticsearch 8.9.0** - Moteur de recherche et analytics
- **Logstash 8.9.0** - Pipeline de traitement de données
- **Redis 7** - Cache et file de messages
- **Kibana 8.9.0** - Visualisation de données

### Frontend
- **Angular 17** - Framework JavaScript
- **TypeScript** - Typage statique
- **RxJS** - Programmation réactive
- **Bootstrap/Material** - UI Components

### DevOps
- **Docker & Docker Compose** - Containerisation
- **Git** - Contrôle de version

## ✨ Fonctionnalités

### 1. Gestion des Alertes
- Monitoring en temps réel des alertes de capteurs
- Classification par sévérité (haute, moyenne, faible)
- Suivi du statut (non résolue, en cours, résolue)
- Statistiques agrégées par catégorie, bâtiment, sévérité

### 2. Données des Capteurs
- Collecte des données de capteurs (température, humidité, CO2, etc.)
- Monitoring de l'état des capteurs (actif, inactif, maintenance)
- Suivi du niveau de batterie
- Historique des calibrations

### 3. Consommation Énergétique
- Suivi de la consommation électrique, eau, gaz
- Analyse par type (climatisation, éclairage, chauffage)
- Calcul du coût estimé et empreinte carbone
- Comparaison avec les périodes précédentes

### 4. Occupation des Salles
- Monitoring de l'occupation en temps réel
- Gestion des réservations et événements
- Calcul du taux d'utilisation
- Suivi des équipements utilisés

### 5. Maintenance Préventive
- Planification des interventions de maintenance
- Prédiction des pannes
- Suivi de la durée de vie des équipements
- Gestion des coûts de maintenance

## 📦 Prérequis

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**
- **Node.js 18+** et **npm** (pour le développement Angular)
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

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est développé dans le cadre d'un projet académique Big Data.

## 👥 Auteurs

Projet Big Data - Système de Gestion IoT

## 🙏 Remerciements

- Elastic Stack (Elasticsearch, Logstash, Kibana)
- Django & Django REST Framework
- Angular Framework
- Docker Community

## 📞 Support

Pour toute question ou problème :
- Consulter la documentation dans [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)
- Vérifier les logs des containers
- Consulter les issues GitHub

---

**Note**: Ce projet nécessite Docker et Docker Compose pour fonctionner. Assurez-vous que tous les ports nécessaires sont disponibles avant de démarrer les services.
