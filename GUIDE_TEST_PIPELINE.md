# Guide de Test du Pipeline Complet

## Architecture du Pipeline

```
┌─────────┐    HTTP POST     ┌────────┐    lpush      ┌───────┐    consume    ┌──────────┐    index    ┌──────────────┐
│ Angular │ ───────────────> │ Django │ ───────────> │ Redis │ ───────────> │ Logstash │ ─────────> │ Elasticsearch│
│   UI    │   FormData       │  API   │   JSON       │ Queue │   JSON       │  Filter  │   JSON     │    Index     │
└─────────┘                  └────────┘              └───────┘              └──────────┘            └──────────────┘
```

## Fichiers de Test Créés

### 1. `test_angular_to_elasticsearch.json`
- **5 alertes** avec IDs uniques (ALT-ANGULAR-001 à 005)
- Types variés: test_angular, incendie, intrusion, temperature, fuite
- Sévérités: critique, haute, moyenne
- **Description**: Contient des messages explicites sur le pipeline

### 2. `test_angular_pipeline_complet.py`
- Script Python qui **simule** l'upload depuis Angular
- Vérifie chaque étape du pipeline
- Affiche l'état de Redis et Elasticsearch en temps réel

## Comment Tester

### Option 1: Test via Angular (UI)

1. **Démarrer Angular**:
   ```bash
   cd angular-app
   npm start
   ```

2. **Ouvrir le navigateur**: http://localhost:4200/upload

3. **Upload du fichier**:
   - Glisser-déposer `test_angular_to_elasticsearch.json`
   - **OU** cliquer sur "Parcourir les fichiers"
   - Sélectionner le type: **🚨 Alertes** (ou laisser Auto)
   - Cliquer sur **"📤 Uploader le fichier"**

4. **Vérifier le résultat**:
   - Message de succès avec détails
   - Nombre d'enregistrements traités: **5**
   - Queue Redis affichée
   - Message: "Pipeline activé: Angular → Django → Redis → Logstash → Elasticsearch"

### Option 2: Test via Script Python

```bash
python test_angular_pipeline_complet.py
```

Le script va:
1. ✓ Vérifier le fichier de test
2. ✓ Compter les documents initiaux dans Elasticsearch
3. ✓ Vérifier l'état de Redis
4. ✓ Uploader via l'API Django (comme Angular)
5. ✓ Surveiller Redis pendant le traitement
6. ✓ Vérifier l'indexation dans Elasticsearch
7. ✓ Afficher un exemple de document indexé

### Option 3: Test via curl

```bash
curl -X POST -F "file=@Fichier_logs/test_angular_to_elasticsearch.json" -F "data_type=alertes" http://localhost:8000/upload/
```

## Vérifications Post-Upload

### 1. Vérifier Redis
```bash
docker exec redis_container redis-cli -a redis_password_123 LLEN "iot:data"
```
- Devrait être **0** (messages consommés par Logstash)

### 2. Vérifier Elasticsearch
```powershell
Invoke-WebRequest -Uri "http://localhost:9200/iot-alertes/_count" | ConvertFrom-Json | Select-Object -ExpandProperty count
```

### 3. Chercher les documents uploadés
```powershell
$query = '{"query":{"match":{"source_file":"test_angular_to_elasticsearch.json"}},"size":1}'
Invoke-WebRequest -Method POST -Uri "http://localhost:9200/iot-alertes/_search" -ContentType "application/json" -Body $query | ConvertFrom-Json
```

### 4. Vérifier les logs Logstash
```bash
docker-compose logs --tail=50 logstash
```

## Améliorations Angular

### Composant FileUpload mis à jour:

1. **Sélecteur de type de données**:
   - 🤖 Détection automatique
   - 🚨 Alertes
   - 📡 Capteurs
   - ⚡ Consommation
   - 👥 Occupation
   - 🔧 Maintenance

2. **Détails de la réponse**:
   - Nom du fichier
   - Type de données
   - Nombre d'enregistrements
   - Longueur de la queue Redis
   - Statut du pipeline

3. **Service uploadFileWithType()**:
   - Envoie le `data_type` en plus du fichier
   - Compatible avec l'API Django modifiée

## Flux de Données Détaillé

### 1. Angular (Frontend)
```typescript
uploadFile() {
  const formData = new FormData();
  formData.append('file', selectedFile);
  formData.append('data_type', 'alertes');
  
  this.http.post('/upload/', formData).subscribe(...)
}
```

### 2. Django API (Backend)
```python
# views.py - FileUploadView
data_type = request.data.get('data_type') or auto_detect(filename)
redis_client.lpush("iot:data", json.dumps({
    "source_file": filename,
    "data_type": data_type,
    "upload_timestamp": now(),
    "data": record
}))
```

### 3. Redis (Queue)
```json
{
  "source_file": "test_angular_to_elasticsearch.json",
  "data_type": "alertes",
  "upload_timestamp": "2025-12-09T10:30:00",
  "data": {
    "id_alerte": "ALT-ANGULAR-001",
    "type_alerte": "test_angular",
    ...
  }
}
```

### 4. Logstash (Processing)
```ruby
# redis-to-elasticsearch.conf
input { redis { key => "iot:data" } }
filter { json { source => "message" } }
output { 
  if [data_type] == "alertes" {
    elasticsearch { index => "iot-alertes" }
  }
}
```

### 5. Elasticsearch (Storage)
```json
{
  "id_alerte": "ALT-ANGULAR-001",
  "type_alerte": "test_angular",
  "source_file": "test_angular_to_elasticsearch.json",
  "data_type": "alertes",
  "upload_timestamp": "2025-12-09T10:30:00",
  ...
}
```

## Dépannage

### Problème: Les documents n'apparaissent pas dans ES

1. **Vérifier Redis**:
   - Si queue > 0 longtemps → Logstash ne consomme pas
   - Si queue = 0 rapidement → Logstash consomme mais n'indexe pas

2. **Vérifier Logstash**:
   ```bash
   docker-compose logs --tail=100 logstash | grep -i "error\|warn"
   ```

3. **Vérifier le document_id**:
   - Les IDs identiques écrasent les anciens documents
   - Solution: IDs uniques (ALT-ANGULAR-XXX)

4. **Rafraîchir l'index ES**:
   ```bash
   curl -X POST http://localhost:9200/iot-alertes/_refresh
   ```

### Problème: Angular ne peut pas uploader

1. **Vérifier CORS** dans Django settings.py:
   ```python
   CORS_ALLOWED_ORIGINS = ["http://localhost:4200"]
   ```

2. **Vérifier l'URL** dans environment.ts:
   ```typescript
   uploadUrl: 'http://localhost:8000/upload'
   ```

3. **Vérifier le service Django**:
   ```bash
   docker-compose ps django
   docker-compose logs django
   ```

## Prochaines Étapes

1. ✅ Upload depuis Angular avec sélection du type
2. ✅ API Django avec routing intelligent
3. ✅ Pipeline Redis → Logstash configuré
4. ⏳ **Vérifier l'indexation finale dans ES**
5. ⏳ Visualiser dans Kibana

## Succès Attendu

Après l'upload, vous devriez voir:
- ✅ Message de succès dans Angular
- ✅ 5 enregistrements traités
- ✅ Queue Redis = 0 (consommée)
- ✅ 5 nouveaux documents dans iot-alertes
- ✅ Documents avec champs: source_file, data_type, upload_timestamp
