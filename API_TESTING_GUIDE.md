# Guide de Test des API IoT

Ce guide contient toutes les requêtes pour tester les API du projet IoT avec Postman ou curl.

## Prérequis

1. Tous les services Docker doivent être démarrés
2. Les données doivent être ingérées dans Elasticsearch

## Import de la Collection Postman

Utilisez le fichier `Postman_Collection.json` à la racine du projet pour importer toutes les requêtes dans Postman.

## Requêtes curl

### Health Check

```bash
curl http://localhost:8000/api/health
```

### API Alertes

#### Récupérer toutes les alertes
```bash
curl "http://localhost:8000/api/alertes?size=10"
```

#### Rechercher des alertes
```bash
curl "http://localhost:8000/api/alertes?q=CO2&size=10"
```

#### Filtrer par sévérité
```bash
curl "http://localhost:8000/api/alertes?severite=haute&size=10"
```

#### Filtrer par statut
```bash
curl "http://localhost:8000/api/alertes?statut=non_resolue&size=10"
```

#### Filtrer par bâtiment
```bash
curl "http://localhost:8000/api/alertes?batiment=Batiment%20A&size=10"
```

#### Multi-filtres
```bash
curl "http://localhost:8000/api/alertes?severite=haute&statut=non_resolue&batiment=Batiment%20A"
```

#### Pagination et tri
```bash
curl "http://localhost:8000/api/alertes?from=0&size=20&sort_by=timestamp&sort_order=desc"
```

#### Statistiques des alertes
```bash
curl http://localhost:8000/api/alertes/stats
```

### API Capteurs

#### Récupérer tous les capteurs
```bash
curl "http://localhost:8000/api/capteurs?size=10"
```

#### Filtrer par type
```bash
curl "http://localhost:8000/api/capteurs?type=temperature&size=10"
```

#### Filtrer par statut
```bash
curl "http://localhost:8000/api/capteurs?statut=actif&size=10"
```

#### Filtrer par bâtiment
```bash
curl "http://localhost:8000/api/capteurs?batiment=Batiment%20A&size=10"
```

#### Statistiques des capteurs
```bash
curl http://localhost:8000/api/capteurs/stats
```

### API Consommation

#### Récupérer toutes les consommations
```bash
curl "http://localhost:8000/api/consommation?size=10"
```

#### Filtrer par type d'énergie
```bash
curl "http://localhost:8000/api/consommation?type_energie=electricite&size=10"
```

#### Filtrer par sous-type
```bash
curl "http://localhost:8000/api/consommation?sous_type=climatisation&size=10"
```

#### Filtrer par bâtiment
```bash
curl "http://localhost:8000/api/consommation?batiment=Batiment%20A&size=10"
```

#### Statistiques de consommation
```bash
curl http://localhost:8000/api/consommation/stats
```

### API Occupation

#### Récupérer toutes les occupations
```bash
curl "http://localhost:8000/api/occupation?size=10"
```

#### Filtrer par type de salle
```bash
curl "http://localhost:8000/api/occupation?type_salle=conference&size=10"
```

#### Filtrer par statut
```bash
curl "http://localhost:8000/api/occupation?statut=occupee&size=10"
```

#### Filtrer par bâtiment
```bash
curl "http://localhost:8000/api/occupation?batiment=Batiment%20A&size=10"
```

#### Statistiques d'occupation
```bash
curl http://localhost:8000/api/occupation/stats
```

### API Maintenance

#### Récupérer toutes les maintenances
```bash
curl "http://localhost:8000/api/maintenance?size=10"
```

#### Filtrer par type d'équipement
```bash
curl "http://localhost:8000/api/maintenance?type_equipement=CVC&size=10"
```

#### Filtrer par type de maintenance
```bash
curl "http://localhost:8000/api/maintenance?type_maintenance=preventive&size=10"
```

#### Filtrer par sévérité
```bash
curl "http://localhost:8000/api/maintenance?severite=critique&size=10"
```

#### Filtrer par bâtiment
```bash
curl "http://localhost:8000/api/maintenance?batiment=Batiment%20A&size=10"
```

#### Statistiques de maintenance
```bash
curl http://localhost:8000/api/maintenance/stats
```

## Requêtes Avancées

### Recherche avec filtres multiples
```bash
curl "http://localhost:8000/api/capteurs?q=temperature&type=temperature&batiment=Batiment%20A&statut=actif"
```

### Pagination avancée
```bash
curl "http://localhost:8000/api/alertes?from=20&size=10&sort_by=severite&sort_order=desc"
```

### Recherche textuelle dans maintenance
```bash
curl "http://localhost:8000/api/maintenance?q=compresseur&size=10"
```

## Format de Réponse

Toutes les API retournent une réponse au format :

```json
{
  "total": 100,
  "count": 10,
  "documents": [...],
  "from": 0,
  "size": 10
}
```

Les API de statistiques retournent :

```json
{
  "total": 100,
  "by_<field>": [
    {"key": "value", "count": 25}
  ],
  ...
}
```

## Paramètres Disponibles

| Paramètre | Type | Description |
|-----------|------|-------------|
| q | string | Recherche textuelle |
| size | integer | Nombre de résultats (défaut: 10) |
| from | integer | Offset de pagination (défaut: 0) |
| sort_by | string | Champ de tri |
| sort_order | string | Ordre de tri (asc/desc) |

### Filtres spécifiques par API

**Alertes:**
- severite: haute, moyenne, faible
- statut: non_resolue, en_cours, resolue
- categorie: qualite_air, temperature, humidite, etc.
- batiment: Batiment A, Batiment B, etc.

**Capteurs:**
- type: temperature, humidite, CO2, etc.
- statut: actif, inactif, maintenance
- batiment: Batiment A, Batiment B, etc.
- zone: Zone Nord, Zone Sud, etc.

**Consommation:**
- type_energie: electricite, eau, gaz
- sous_type: climatisation, eclairage, chauffage, etc.
- batiment: Batiment A, Batiment B, etc.

**Occupation:**
- type_salle: conference, bureau, laboratoire, etc.
- statut: occupee, libre, reservee
- batiment: Batiment A, Batiment B, etc.

**Maintenance:**
- type_equipement: CVC, Ascenseur, Eclairage, etc.
- type_maintenance: preventive, corrective, predictive
- severite: critique, moyenne, faible
- batiment: Batiment A, Batiment B, etc.

## Exemples PowerShell

Pour Windows PowerShell:

```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:8000/api/health" | Select-Object -ExpandProperty Content | ConvertFrom-Json

# Alertes avec filtres
$response = Invoke-WebRequest -Uri "http://localhost:8000/api/alertes?severite=haute&size=10"
$data = $response.Content | ConvertFrom-Json
$data.documents | Format-Table

# Statistiques
Invoke-WebRequest -Uri "http://localhost:8000/api/capteurs/stats" | Select-Object -ExpandProperty Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

## Dépannage

### Si les API ne retournent pas de données:

1. Vérifier qu'Elasticsearch contient des données:
```bash
curl http://localhost:9200/_cat/indices?v
```

2. Vérifier qu'un index spécifique contient des documents:
```bash
curl http://localhost:9200/iot-alertes/_count
curl http://localhost:9200/iot-capteurs/_count
curl http://localhost:9200/iot-consommation/_count
curl http://localhost:9200/iot-occupation/_count
curl http://localhost:9200/iot-maintenance/_count
```

3. Vérifier les logs Django:
```bash
docker logs django_container --tail 50
```

4. Vérifier les logs Logstash:
```bash
docker logs logstash_container --tail 100
```

### Pour réinitialiser et réingérer les données:

```bash
# Supprimer tous les indices
curl -X DELETE http://localhost:9200/iot-*

# Redémarrer Logstash pour réingérer
docker restart logstash_container

# Attendre 30-40 secondes puis vérifier
curl http://localhost:9200/_cat/indices?v
```
