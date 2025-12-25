# 🏢 Plateforme IoT Big Data - Documentation Complète

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Angular](https://img.shields.io/badge/Angular-17-red.svg)](https://angular.io/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.9-yellow.svg)](https://www.elastic.co/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

**Plateforme complète de gestion et d'analyse de données IoT pour le monitoring intelligent de bâtiments**

---

## 📋 Table des Matières

1. [Vue d'ensemble](#-vue-densemble)
2. [Architecture](#-architecture)
3. [Technologies](#-technologies)
4. [Fonctionnalités](#-fonctionnalités)
5. [Installation](#-installation-rapide)
6. [Utilisation](#-guide-dutilisation)
7. [API](#-api-rest)
8. [Structure](#-structure-du-projet)
9. [Tests](#-tests)
10. [Dépannage](#-dépannage)

---

## 🎯 Vue d'ensemble

Cette plateforme Big Data permet de collecter, traiter, stocker et analyser des données IoT en temps réel provenant de bâtiments intelligents. Elle couvre **5 domaines** :

1. **Alertes** : Détection d'anomalies des capteurs
2. **Capteurs** : Monitoring environnemental (température, humidité, CO2...)
3. **Consommation** : Suivi énergétique (électricité, eau, gaz)
4. **Occupation** : Gestion d'espaces et salles
5. **Maintenance** : Interventions préventives et correctives

### Flux de données

```
Fichiers IoT → Django Upload API → Redis Queue → Logstash ETL → Elasticsearch
                                                                        ↓
                     Angular Frontend ← Django REST API ← Elasticsearch
```

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                    PLATEFORME IOT BIG DATA                        │
└───────────────────────────────────────────────────────────────────┘

┌─────────────┐     ┌──────────┐     ┌───────┐     ┌──────────┐
│  Fichiers   │────▶│  Django  │────▶│ Redis │────▶│ Logstash │
│  CSV/JSON   │     │ Upload   │     │ Queue │     │ Pipeline │
└─────────────┘     └──────────┘     └───────┘     └─────┬────┘
                                                           │
┌─────────────┐     ┌──────────┐     ┌──────────────────┴────┐
│   Angular   │◀────│  Django  │◀────│   Elasticsearch       │
│  Frontend   │     │ REST API │     │   (5 indices IoT)     │
└──────┬──────┘     └──────────┘     └───────────────────────┘
       │                                        ▲
       ▼                                        │
┌─────────────┐                          ┌─────┴──────┐
│   Kibana    │─────────────────────────▶│    Search  │
│  Dashboard  │                          │  Analytics │
└─────────────┘                          └────────────┘
```

### Conteneurs Docker

| Service | Image | Rôle |
|---------|-------|------|
| **Elasticsearch** | 8.9.0 | Stockage et recherche |
| **Kibana** | 8.9.0 | Visualisation |
| **Logstash** | 8.9.0 | Pipeline ETL |
| **Redis** | 7.0 | Queue de messages |
| **Django** | Python 3.11 | API REST Backend |

---

## 🛠️ Technologies

### Backend

- **Python 3.11** - Langage principal
- **Django 5.0** - Framework web
- **Django REST Framework 3.14** - API RESTful
- **elasticsearch-py** - Client Elasticsearch
- **redis-py** - Client Redis

### Elastic Stack

- **Elasticsearch 8.9.0** - Moteur de recherche distribué
- **Logstash 8.9.0** - Pipeline ETL (Extract, Transform, Load)
- **Kibana 8.9.0** - Interface de visualisation
- **Redis 7.0** - File d'attente et cache

### Frontend

- **Angular 17** - Framework SPA
- **TypeScript 5.2** - Typage statique
- **RxJS 7.8** - Programmation réactive
- **SCSS** - Préprocesseur CSS

### DevOps

- **Docker 24+** - Containerisation
- **Docker Compose 2.0+** - Orchestration
- **Git** - Contrôle de version

---

## ✨ Fonctionnalités

### 🚨 Alertes IoT
- Classification par sévérité (critique, haute, moyenne, faible)
- Suivi statut (non résolue, en cours, résolue, fermée)
- Catégorisation (anomalie, défaillance, seuil dépassé, maintenance)
- Statistiques temps réel par bâtiment/zone

### 📡 Capteurs
- Multi-types : température, humidité, CO2, luminosité, mouvement
- Monitoring état : actif, inactif, maintenance, défaillant
- Suivi batterie avec alertes niveau faible
- Historique calibrations et dérive

### ⚡ Consommation Énergétique
- Électricité, eau, gaz
- Sous-catégories : climatisation, éclairage, chauffage
- Calcul coûts (€) et empreinte carbone (kg CO2)
- Détection surconsommation

### 👥 Occupation Salles
- Temps réel et historique
- Gestion réservations/événements
- Taux d'utilisation
- Optimisation capacité

### 🔧 Maintenance
- Préventive, corrective, prédictive
- Prioritisation par sévérité
- Suivi durée de vie équipements
- Analyse coûts

### 🔍 Recherche Avancée
- Full-text search sur tous les champs
- Filtres multiples combinables
- Agrégations statistiques temps réel
- Top 3 résultats avec médailles (🥇🥈🥉)
- Recherche floue (tolérance fautes)

### 📊 Interface Angular
- Upload drag & drop
- Détection automatique type de données
- Dashboard interactif
- Refresh auto après upload
- Intégration Kibana

---

## 🚀 Installation Rapide

### Prérequis

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **8 GB RAM** minimum
- **10 GB disque** libre

### Ports requis

| Port | Service | Accès |
|------|---------|-------|
| 8000 | Django API | http://localhost:8000 |
| 4200 | Angular | http://localhost:4200 |
| 9200 | Elasticsearch | http://localhost:9200 |
| 5601 | Kibana | http://localhost:5601 |
| 6379 | Redis | localhost:6379 |

### Installation en 5 étapes

#### 1️⃣ Cloner le projet

```bash
git clone <repository-url>
cd Projet
```

#### 2️⃣ Démarrer tous les services

```bash
docker-compose up -d
```

#### 3️⃣ Vérifier le statut

```bash
docker-compose ps
```

Tous doivent afficher "Up".

#### 4️⃣ Attendre l'initialisation (30-60s)

```bash
# Suivre les logs
docker-compose logs -f elasticsearch

# Attendre le message:
# "Cluster health status changed from [YELLOW] to [GREEN]"
```

#### 5️⃣ Lancer les tests

```bash
python test_complet.py
```

Si tous les tests passent ✅, l'installation est réussie !

---

## 📖 Guide d'utilisation

### Accès aux interfaces

- **Angular (Users)** : http://localhost:4200
- **Django API (Dev)** : http://localhost:8000/api/
- **Kibana (Analytics)** : http://localhost:5601

### Upload de fichiers

#### Méthode 1 : Interface Angular

1. Ouvrir http://localhost:4200
2. Drag & drop un fichier CSV/JSON
3. Sélectionner le type (ou "auto")
4. Cliquer "Uploader"

#### Méthode 2 : API avec curl

```bash
# Upload alertes
curl -X POST http://localhost:8000/upload/ \
  -F "file=@Fichier_logs/logs_alertes.json" \
  -F "data_type=alertes"

# Upload capteurs
curl -X POST http://localhost:8000/upload/ \
  -F "file=@Fichier_logs/logs_capteurs.csv" \
  -F "data_type=capteurs"
```

#### Méthode 3 : Script Python

```python
import requests

with open('Fichier_logs/logs_alertes.json', 'rb') as f:
    files = {'file': f}
    data = {'data_type': 'alertes'}
    r = requests.post('http://localhost:8000/upload/', files=files, data=data)
    print(r.json())
```

### Recherche de données

#### Recherche simple

```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "batiment A", "size": 10}'
```

#### Recherche avec filtres

```bash
# Alertes critiques
curl "http://localhost:8000/api/alertes/?severite=critique&size=20"

# Capteurs en maintenance
curl "http://localhost:8000/api/capteurs/?statut=maintenance"

# Surconsommation électrique
curl "http://localhost:8000/api/consommation/?type_energie=electricite&valeur_min=50"
```

### Vérifier les données Elasticsearch

```bash
# Lister les indices
curl http://localhost:9200/_cat/indices?v

# Compter les documents
curl http://localhost:9200/iot-alertes/_count
curl http://localhost:9200/iot-capteurs/_count
curl http://localhost:9200/iot-consommation/_count
```

---

## 🔌 API REST

### Format de réponse standard

```json
{
  "total": 100,
  "count": 10,
  "documents": [...],
  "from": 0,
  "size": 10
}
```

### Endpoints principaux

#### Health Check
```http
GET /api/health/
```

**Réponse** :
```json
{
  "status": "healthy",
  "services": {
    "elasticsearch": "connected",
    "redis": "connected",
    "redis_queue_length": 0
  }
}
```

#### Recherche globale
```http
POST /api/search/
Content-Type: application/json

{
  "query": "batiment A",
  "size": 20,
  "from": 0
}
```

#### Alertes
```http
GET /api/alertes/?severite=haute&batiment=Batiment+A&size=20
GET /api/alertes/stats
```

**Paramètres** :
- `q` : Recherche textuelle
- `size` : Nb résultats (1-100)
- `from` : Offset pagination
- `severite` : critique, haute, moyenne, faible
- `statut` : non_resolue, en_cours, resolue, fermee
- `categorie` : anomalie, defaillance, seuil_depasse
- `batiment` : Batiment A, B, C...
- `sort_by`, `sort_order`

#### Capteurs
```http
GET /api/capteurs/?type=temperature&statut=actif
GET /api/capteurs/stats
```

**Paramètres** :
- `type` : temperature, humidite, co2, luminosite, mouvement
- `statut` : actif, inactif, maintenance, defaillant
- `batiment`, `zone`, `etage`
- `niveau_batterie_min`, `niveau_batterie_max`

#### Consommation
```http
GET /api/consommation/?type_energie=electricite&valeur_min=50
GET /api/consommation/stats
```

**Paramètres** :
- `type_energie` : electricite, eau, gaz
- `sous_type` : climatisation, eclairage, chauffage
- `valeur_min`, `valeur_max`

#### Occupation
```http
GET /api/occupation/?type_salle=reunion&statut=occupe
GET /api/occupation/stats
```

**Paramètres** :
- `type_salle` : reunion, bureau, laboratoire, salle_cours
- `statut` : libre, occupe, reserve, maintenance
- `taux_occupation_min`, `taux_occupation_max`

#### Maintenance
```http
GET /api/maintenance/?type_maintenance=preventive&severite=haute
GET /api/maintenance/stats
```

**Paramètres** :
- `type_equipement` : hvac, eclairage, securite, informatique
- `type_maintenance` : preventive, corrective, predictive
- `severite` : critique, haute, moyenne, faible

### Exemples curl complets

```bash
# Alertes critiques récentes
curl "http://localhost:8000/api/alertes/?severite=critique&sort_by=timestamp&sort_order=desc&size=10"

# Capteurs batterie faible
curl "http://localhost:8000/api/capteurs/?niveau_batterie_max=20&sort_by=niveau_batterie"

# Top consommations
curl "http://localhost:8000/api/consommation/?sort_by=valeur_consommation&sort_order=desc&size=10"

# Salles occupées
curl "http://localhost:8000/api/occupation/?statut=occupe&sort_by=taux_occupation&sort_order=desc"
```

---

## 📁 Structure du Projet

```
Projet/
├── 📂 django_app/              Backend Django
│   ├── api/                    Application API
│   │   ├── views.py           10 vues API
│   │   ├── serializers.py     Validation données
│   │   ├── elasticsearch_service.py  Service ES
│   │   └── models.py          Models Django
│   ├── config/                Configuration
│   │   ├── settings.py        Settings Django
│   │   └── urls.py            Routage URL
│   ├── requirements.txt       Dépendances Python
│   └── Dockerfile             Image Django
│
├── 📂 angular-app/            Frontend Angular
│   ├── src/app/
│   │   ├── components/        Composants UI
│   │   │   ├── dashboard/
│   │   │   ├── file-upload/
│   │   │   └── ...
│   │   ├── services/          Services HTTP
│   │   │   ├── api.service.ts
│   │   │   ├── file-upload.service.ts
│   │   │   └── elasticsearch-search.service.ts
│   │   └── models/            Interfaces TypeScript
│   ├── package.json
│   └── angular.json
│
├── 📂 logstash/               Configuration Logstash
│   ├── pipeline/              5 pipelines
│   │   ├── redis-to-elasticsearch.conf  Pipeline principal
│   │   ├── alertes-to-elasticsearch.conf
│   │   ├── capteurs-to-elasticsearch.conf
│   │   ├── consommation-to-elasticsearch.conf
│   │   └── occupation-to-elasticsearch.conf
│   └── config/
│       └── logstash.yaml
│
├── 📂 Fichier_logs/           Fichiers sources
│   ├── logs_alertes.json      Alertes (JSON)
│   ├── logs_capteurs.csv      Capteurs (CSV)
│   ├── logs_consommation.json Consommation (JSON)
│   ├── logs_occupation.csv    Occupation (CSV)
│   └── logs_maintenance.csv   Maintenance (CSV)
│
├── 📂 redis/                  Configuration Redis
│   └── redis.conf
│
├── 📄 docker-compose.yaml     Orchestration Docker
├── 📄 test_complet.py         Script de test complet
└── 📄 README.md              Cette documentation
```

### Fichiers de configuration clés

| Fichier | Description |
|---------|-------------|
| `docker-compose.yaml` | Orchestration des 5 services |
| `django_app/config/settings.py` | Config Django + ES + Redis |
| `logstash/pipeline/*.conf` | Pipelines de transformation |
| `angular-app/src/environments/` | URLs des services |

---

## 🧪 Tests

### Script de test complet

Le projet inclut un script de test unifié :

```bash
# Test complet (services + upload + recherche)
python test_complet.py

# Tests rapides uniquement
python test_complet.py --quick

# Tester uniquement les services
python test_complet.py --services

# Tester uniquement l'upload
python test_complet.py --upload

# Tester uniquement la recherche
python test_complet.py --search
```

### Ce qui est testé

#### ✅ Services
- Elasticsearch accessible et healthy
- Kibana opérationnel
- Redis connecté
- Django API répond
- Angular accessible

#### ✅ Upload
- Upload fichiers JSON
- Upload fichiers CSV
- Upload avec détection auto
- Mise en queue Redis
- Traitement Logstash

#### ✅ Indexation
- Données dans Elasticsearch
- Comptage documents par index
- Structure des données

#### ✅ API
- Endpoints de recherche
- Endpoints de statistiques
- Pagination
- Filtres
- Tri

### Exemples de tests manuels

```bash
# Test 1: Services actifs
curl http://localhost:9200
curl http://localhost:8000/api/health/
curl http://localhost:5601

# Test 2: Upload
curl -X POST http://localhost:8000/upload/ \
  -F "file=@Fichier_logs/test_alertes_upload.json" \
  -F "data_type=alertes"

# Test 3: Vérifier indexation (attendre 10s)
curl http://localhost:9200/iot-alertes/_count

# Test 4: Recherche API
curl "http://localhost:8000/api/alertes/?size=5"

# Test 5: Statistiques
curl http://localhost:8000/api/statistics/
```

---

## 🔧 Dépannage

### Problèmes courants

#### ❌ Services ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs -f

# Redémarrer
docker-compose restart

# Reconstruire
docker-compose up -d --build
```

#### ❌ Elasticsearch indisponible

```bash
# Vérifier le statut
curl http://localhost:9200/_cluster/health

# Redémarrer ES
docker-compose restart elasticsearch

# Attendre 30s puis revérifier
```

#### ❌ Pas de données dans Elasticsearch

```bash
# Vérifier la queue Redis
docker-compose exec redis redis-cli -a redis_password_123 LLEN iot:data

# Vérifier les logs Logstash
docker-compose logs logstash | grep -i error

# Redémarrer Logstash
docker-compose restart logstash
```

#### ❌ API Django erreurs

```bash
# Logs Django
docker-compose logs django

# Vérifier variables env
docker-compose exec django env | grep ELASTICSEARCH

# Redémarrer Django
docker-compose restart django
```

#### ❌ Upload échoue

```bash
# Vérifier logs Django
docker-compose logs django --tail 50

# Tester manuellement
curl -X POST http://localhost:8000/upload/ \
  -F "file=@Fichier_logs/test_alertes_upload.json" \
  -F "data_type=alertes" -v
```

#### ❌ Angular ne charge pas

```bash
# Redémarrer le dev server
cd angular-app
npm start

# Ou en mode production
ng serve --configuration production
```

### Réinitialisation complète

```bash
# Arrêter tous les services
docker-compose down

# Supprimer les volumes (ATTENTION: perte de données)
docker-compose down -v

# Nettoyer les images
docker system prune -a

# Redémarrer proprement
docker-compose up -d
```

### Vérifications de santé

```bash
# Status global
docker-compose ps

# Santé Elasticsearch
curl http://localhost:9200/_cluster/health?pretty

# Santé Django
curl http://localhost:8000/api/health/

# Queue Redis
docker-compose exec redis redis-cli -a redis_password_123 INFO
```

### Logs utiles

```bash
# Tous les logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f elasticsearch
docker-compose logs -f logstash
docker-compose logs -f django

# Dernières 100 lignes
docker-compose logs --tail 100 logstash
```

---

## 📊 Performance et optimisation

### Configuration Elasticsearch

Pour production, modifier `docker-compose.yaml` :

```yaml
elasticsearch:
  environment:
    - "ES_JAVA_OPTS=-Xms4g -Xmx4g"  # 4GB heap
  deploy:
    resources:
      limits:
        memory: 8G
```

### Indexation par batch

Pour upload massif :

```python
import requests
import json
from pathlib import Path

files_to_upload = [
    ('logs_alertes.json', 'alertes'),
    ('logs_capteurs.csv', 'capteurs'),
    ('logs_consommation.json', 'consommation'),
    ('logs_occupation.csv', 'occupation'),
    ('logs_maintenance.csv', 'maintenance')
]

for filename, data_type in files_to_upload:
    filepath = Path(f'Fichier_logs/{filename}')
    with open(filepath, 'rb') as f:
        files = {'file': f}
        data = {'data_type': data_type}
        r = requests.post('http://localhost:8000/upload/', files=files, data=data)
        print(f'{filename}: {r.json()}')
```

---

## 🤝 Contribution

Contributions bienvenues ! 

1. Fork le projet
2. Créer une branche : `git checkout -b feature/AmazingFeature`
3. Commit : `git commit -m 'Add AmazingFeature'`
4. Push : `git push origin feature/AmazingFeature`
5. Ouvrir une Pull Request

---

## 📝 License

Projet académique Big Data - Système de Gestion IoT

---

## 👥 Support

- **Documentation** : Ce fichier README.md
- **Tests** : `python test_complet.py`
- **Logs** : `docker-compose logs -f`
- **Health** : http://localhost:8000/api/health/

---

## 🎓 Crédits

Technologies utilisées :
- **Elastic Stack** (Elasticsearch, Logstash, Kibana)
- **Django** & Django REST Framework
- **Angular** Framework
- **Redis** Database
- **Docker** Container Platform

---

**Date de dernière mise à jour** : Décembre 2025

**Version** : 1.0.0

🚀 **Bon développement !**
