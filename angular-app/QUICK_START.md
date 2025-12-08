# 🎯 Guide de Démarrage Rapide - Application Angular IoT Dashboard

## ⚡ Lancement Rapide

### Windows
```bash
start-angular.bat
```

### Linux / Mac
```bash
chmod +x start-angular.sh
./start-angular.sh
```

## 📋 Prérequis

- ✅ **Node.js 18+** installé ([Télécharger](https://nodejs.org/))
- ✅ **npm 9+** (inclus avec Node.js)
- ✅ **Backend Django** en cours d'exécution (`docker-compose up -d`)

## 🚀 Installation Manuelle

Si les scripts ne fonctionnent pas, suivez ces étapes:

```bash
# 1. Aller dans le dossier Angular
cd angular-app

# 2. Installer les dépendances
npm install

# 3. Démarrer l'application
npm start
```

L'application sera accessible sur: **http://localhost:4200**

## 📊 Architecture de l'Application

```
┌─────────────────────────────────────────────────────────┐
│                    Angular Frontend                     │
│                   (Port 4200)                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Dashboard  │  │   Devices   │  │   Sensors   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐                     │
│  │  Vehicles   │  │ File Upload │                     │
│  └─────────────┘  └─────────────┘                     │
│                                                         │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP REST API
                     │
┌────────────────────▼────────────────────────────────────┐
│                 Django Backend                          │
│                  (Port 8000)                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │    Redis    │  │Elasticsearch│  │   Logstash  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🎨 Fonctionnalités Implémentées

### ✅ Dashboard
- Vue d'ensemble avec statistiques globales
- Health check (Redis, Elasticsearch)
- Graphiques par type de fichier et statut
- Timeline des uploads
- Table des fichiers sources

### ✅ Devices
- Liste paginée de tous les devices
- Recherche textuelle multi-champs
- Filtres avancés (type, statut, source)
- Tri dynamique sur toutes les colonnes
- Export CSV des résultats
- Vue détaillée par device

### ✅ Sensors (Capteurs)
- Cartes individuelles pour chaque capteur
- Statistiques en temps réel (température, humidité, batterie)
- Indicateurs visuels colorés selon les seuils
- Filtres par location et statut
- Pagination

### ✅ Vehicles (Véhicules)
- Cartes avec informations complètes
- Métriques de vitesse et carburant avec barres de progression
- Coordonnées GPS affichées
- Filtres par conducteur et statut
- Pagination

### ✅ File Upload
- Interface drag & drop intuitive
- Validation des fichiers (CSV/JSON, max 10MB)
- Barre de progression d'upload
- Historique complet des uploads
- Statistiques d'upload

## 🔗 Endpoints API Utilisés

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/health/` | GET | Health check système |
| `/api/stats/` | GET | Statistiques globales |
| `/api/devices/` | GET | Liste des devices |
| `/api/sensors/` | GET | Liste des capteurs |
| `/api/sensors/statistics/` | GET | Stats capteurs |
| `/api/vehicles/` | GET | Liste des véhicules |
| `/api/vehicles/statistics/` | GET | Stats véhicules |
| `/upload/` | POST | Upload de fichiers |
| `/api/files/recent/` | GET | Historique uploads |
| `/api/files/stats/` | GET | Stats uploads |
| `/api/search/` | POST | Recherche avancée |
| `/api/aggregations/` | POST | Agrégations dynamiques |

## 🎯 Navigation

```
┌────────────────────────────────────────────────────┐
│              IoT Dashboard - Navbar                │
├────────────────────────────────────────────────────┤
│  Dashboard | Devices | Sensors | Vehicles | Upload │
└────────────────────────────────────────────────────┘
```

### Routes

- **/** - Dashboard (page d'accueil)
- **/devices** - Liste de tous les devices
- **/sensors** - Gestion des capteurs
- **/vehicles** - Gestion des véhicules
- **/upload** - Upload de fichiers CSV/JSON

## 🎨 Palette de Couleurs

### Gradients Principaux

```scss
// Primary (Bleu)
background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);

// Success (Vert)
background: linear-gradient(135deg, #10b981 0%, #059669 100%);

// Warning (Orange)
background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);

// Danger (Rouge)
background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);

// Purple
background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);

// Navbar
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Badges Statuts

| Statut | Couleur | Classe |
|--------|---------|--------|
| Active | Vert | `badge-success` |
| Warning | Jaune | `badge-warning` |
| Critical | Rouge | `badge-danger` |
| Info / En Route | Bleu | `badge-info` |
| Inactive | Gris | `badge-secondary` |

## 🔧 Configuration

### Environnement de Développement

Fichier: `src/environments/environment.ts`

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',
  uploadUrl: 'http://localhost:8000/upload'
};
```

### Environnement de Production

Fichier: `src/environments/environment.prod.ts`

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-api-domain.com/api',
  uploadUrl: 'https://your-api-domain.com/upload'
};
```

## 📦 Dépendances Principales

```json
{
  "dependencies": {
    "@angular/core": "^18.0.0",
    "@angular/common": "^18.0.0",
    "@angular/router": "^18.0.0",
    "@angular/forms": "^18.0.0",
    "rxjs": "~7.8.0",
    "tslib": "^2.3.0",
    "zone.js": "~0.14.3"
  }
}
```

## 🐛 Résolution de Problèmes

### Erreur: "Cannot find module '@angular/core'"

```bash
cd angular-app
rm -rf node_modules package-lock.json
npm install
```

### Erreur CORS

Vérifiez que Django CORS est configuré dans `django_app/config/settings.py`:

```python
CORS_ALLOW_ALL_ORIGINS = True  # Development only!
```

### Backend non accessible

```bash
# Vérifier les conteneurs Docker
docker-compose ps

# Redémarrer les services
docker-compose restart

# Vérifier les logs
docker-compose logs django
```

### Port 4200 déjà utilisé

```bash
# Changer le port dans angular.json ou utiliser:
ng serve --port 4201
```

## 📊 Build de Production

```bash
# Build optimisé
npm run build

# Les fichiers seront dans: dist/angular-app/

# Pour servir en production
npm install -g http-server
cd dist/angular-app
http-server -p 8080
```

## 🚀 Prochaines Améliorations Possibles

- [ ] Intégration de Chart.js pour graphiques avancés
- [ ] Carte interactive avec Leaflet pour positions GPS
- [ ] WebSocket pour mises à jour en temps réel
- [ ] Authentification JWT
- [ ] Dark mode
- [ ] Notifications push
- [ ] Export PDF des rapports
- [ ] Gestion des utilisateurs et rôles
- [ ] Tests unitaires et E2E
- [ ] Progressive Web App (PWA)

## 📝 Licence

Projet éducatif - BigData

---

**Bon développement! 🚀**
