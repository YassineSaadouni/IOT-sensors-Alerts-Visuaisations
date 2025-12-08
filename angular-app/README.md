# 🚀 Guide de Démarrage - Application Angular IoT Dashboard

## 📦 Installation

### 1. Installer les dépendances Node.js

```bash
cd angular-app
npm install
```

### 2. Démarrer l'application

```bash
npm start
```

L'application sera accessible sur: **http://localhost:4200**

---

## 🎨 Structure de l'Application

```
angular-app/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── dashboard/         # Dashboard principal avec statistiques
│   │   │   ├── devices/           # Liste et recherche de devices
│   │   │   ├── sensors/           # Gestion des capteurs
│   │   │   ├── vehicles/          # Gestion des véhicules
│   │   │   ├── file-upload/       # Upload de fichiers CSV/JSON
│   │   │   └── navbar/            # Navigation
│   │   ├── services/
│   │   │   ├── api.service.ts       # Service API général
│   │   │   ├── device.service.ts    # Service devices
│   │   │   ├── sensor.service.ts    # Service sensors
│   │   │   ├── vehicle.service.ts   # Service vehicles
│   │   │   └── file-upload.service.ts # Service upload
│   │   ├── models/
│   │   │   └── models.ts           # Interfaces TypeScript
│   │   ├── app.module.ts
│   │   ├── app-routing.module.ts
│   │   └── app.component.ts
│   ├── environments/
│   │   ├── environment.ts          # Config dev
│   │   └── environment.prod.ts     # Config prod
│   ├── styles.scss                 # Styles globaux
│   ├── index.html
│   └── main.ts
├── angular.json
├── package.json
└── tsconfig.json
```

---

## 🔧 Configuration

### Environnements

**`src/environments/environment.ts`**
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api',     // Backend Django
  uploadUrl: 'http://localhost:8000/upload'
};
```

---

## 📱 Fonctionnalités Implémentées

### ✅ Dashboard
- Statistiques globales en temps réel
- Health check (Redis, Elasticsearch)
- Graphiques par type de fichier
- Graphiques par statut
- Timeline des uploads
- Table des fichiers sources

### ✅ Services
- **ApiService**: Health check, statistiques, agrégations
- **DeviceService**: CRUD devices avec recherche/filtres
- **SensorService**: Liste capteurs + statistiques
- **VehicleService**: Liste véhicules + statistiques
- **FileUploadService**: Upload fichiers + historique

### ✅ Models
- Interfaces TypeScript complètes
- Types pour API responses
- Models pour Device, Sensor, Vehicle
- Types pour Statistics, Health, Aggregations

---

## 🎯 Composants à Compléter

Pour finaliser l'application, il faut créer les composants suivants:

### 1. DevicesComponent
```bash
ng generate component components/devices
```

**Fonctionnalités:**
- Liste paginée des devices
- Recherche textuelle
- Filtres (file_type, source_file, status)
- Tri dynamique
- Vue détail device

### 2. SensorsComponent
```bash
ng generate component components/sensors
```

**Fonctionnalités:**
- Liste des capteurs
- Statistiques (température, humidité)
- Filtres par location, status
- Graphiques de stats

### 3. VehiclesComponent
```bash
ng generate component components/vehicles
```

**Fonctionnalités:**
- Liste des véhicules
- Carte avec positions GPS
- Statistiques (vitesse, fuel)
- Filtres par driver, status

### 4. FileUploadComponent
```bash
ng generate component components/file-upload
```

**Fonctionnalités:**
- Drag & drop upload
- Validation fichiers (CSV/JSON)
- Progress bar
- Historique des uploads
- Statistiques upload

---

## 🚀 Commandes NPM

```bash
# Développement
npm start              # Démarre le serveur dev (port 4200)
npm run build          # Build de production
npm run watch          # Build avec watch mode
npm test               # Lance les tests

# Build de production
npm run build -- --configuration production

# Analyser le bundle
npm run build -- --stats-json
```

---

## 🔗 Intégration avec le Backend

### 1. S'assurer que le backend Django tourne

```bash
cd ../
docker-compose up -d
```

### 2. Vérifier la connexion

```bash
curl http://localhost:8000/api/health/
```

### 3. Configurer CORS (déjà fait dans Django)

Le backend Django a déjà CORS configuré pour accepter toutes les origines en développement.

---

## 📊 Exemples d'Utilisation des Services

### Dashboard Component (déjà implémenté)

```typescript
ngOnInit(): void {
  // Charger les statistiques
  this.apiService.getStatistics().subscribe(stats => {
    this.stats = stats;
  });

  // Health check
  this.apiService.getHealth().subscribe(health => {
    this.health = health;
  });
}
```

### Devices Component (à créer)

```typescript
ngOnInit(): void {
  // Charger les devices
  this.deviceService.getDevices({ size: 50 }).subscribe(response => {
    this.devices = response.documents;
    this.total = response.total;
  });
}

search(): void {
  const params = {
    query: this.searchQuery,
    size: 50,
    file_type: this.selectedFileType
  };
  
  this.deviceService.getDevices(params).subscribe(response => {
    this.devices = response.documents;
  });
}
```

### Sensors Component (à créer)

```typescript
ngOnInit(): void {
  // Liste des capteurs
  this.sensorService.getSensors({ size: 50 }).subscribe(response => {
    this.sensors = response.documents;
  });

  // Statistiques
  this.sensorService.getStatistics().subscribe(stats => {
    this.temperatureStats = stats.temperature_stats;
    this.humidityStats = stats.humidity_stats;
  });
}
```

### File Upload Component (à créer)

```typescript
onFileSelect(event: any): void {
  const file = event.target.files[0];
  
  this.fileUploadService.uploadFile(file).subscribe({
    next: (response) => {
      console.log('Upload réussi:', response);
      this.loadHistory();
    },
    error: (error) => {
      console.error('Erreur upload:', error);
    }
  });
}
```

---

## 🎨 Styles Disponibles

### Classes CSS Utilitaires

```html
<!-- Cards -->
<div class="card">
  <div class="card-header">Titre</div>
  <p>Contenu</p>
</div>

<!-- Grids -->
<div class="grid grid-2">...</div>  <!-- 2 colonnes -->
<div class="grid grid-3">...</div>  <!-- 3 colonnes -->
<div class="grid grid-4">...</div>  <!-- 4 colonnes -->

<!-- Buttons -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>

<!-- Badges -->
<span class="badge badge-success">Active</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-danger">Critical</span>
<span class="badge badge-info">Info</span>

<!-- Stat Cards -->
<div class="stat-card blue">
  <div class="stat-label">Label</div>
  <div class="stat-value">123</div>
</div>
```

---

## 🐛 Debugging

### Vérifier la connexion API

Ouvrir la console du navigateur (F12) et vérifier:
- Network tab pour voir les requêtes HTTP
- Console pour les erreurs JavaScript
- Application > Local Storage pour les données stockées

### Erreurs courantes

1. **CORS Error**
   - Vérifier que Django CORS est configuré
   - Vérifier l'URL de l'API dans `environment.ts`

2. **404 Not Found**
   - Vérifier que le backend Django tourne
   - Vérifier les URLs dans les services

3. **TypeScript Errors**
   - Installer les dépendances: `npm install`
   - Vérifier `tsconfig.json`

---

## 📚 Ressources

- [Angular Documentation](https://angular.io/docs)
- [RxJS Documentation](https://rxjs.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Chart.js](https://www.chartjs.org/) (pour les graphiques avancés)

---

## 🎉 Prochaines Étapes

1. ✅ **Dashboard** - Implémenté
2. ⏳ **Devices Component** - À créer
3. ⏳ **Sensors Component** - À créer
4. ⏳ **Vehicles Component** - À créer
5. ⏳ **File Upload Component** - À créer
6. 📊 **Charts avancés** - Intégrer Chart.js
7. 🗺️ **Carte GPS** - Intégrer Leaflet pour véhicules
8. 🔐 **Authentication** - Ajouter login/logout
9. 📱 **Responsive Design** - Mobile-friendly
10. 🚀 **Déploiement** - Build de production

---

**L'infrastructure Angular est prête! Il suffit de compléter les composants restants en suivant les exemples fournis.** 🚀
