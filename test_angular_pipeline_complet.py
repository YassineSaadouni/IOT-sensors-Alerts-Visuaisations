"""
Script de test end-to-end du pipeline complet:
Angular → Django API → Redis → Logstash → Elasticsearch

Ce script simule l'upload depuis Angular et vérifie le flux complet
"""

import requests
import json
import time
import sys
import redis
from pathlib import Path
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
API_URL = "http://localhost:8000/upload/"
ES_URL = "http://localhost:9200"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "redis_password_123"

# Fichier de test
TEST_FILE = Path("Fichier_logs/test_angular_to_elasticsearch.json")

print("="*80)
print("TEST END-TO-END: Angular → Django → Redis → Logstash → Elasticsearch")
print("="*80)

# Étape 1: Vérifier que le fichier existe
print(f"\n[1] Vérification du fichier de test...")
if not TEST_FILE.exists():
    print(f"❌ Fichier non trouvé: {TEST_FILE}")
    exit(1)
print(f"✓ Fichier trouvé: {TEST_FILE}")

# Lire le contenu
with open(TEST_FILE, 'r', encoding='utf-8') as f:
    test_data = json.load(f)
print(f"✓ {len(test_data)} alertes dans le fichier")
print(f"  IDs: {', '.join([a['id_alerte'] for a in test_data])}")

# Étape 2: Compter les documents initiaux dans Elasticsearch
print(f"\n[2] État initial Elasticsearch...")
try:
    response = requests.get(f"{ES_URL}/iot-alertes/_count")
    initial_count = response.json()['count']
    print(f"✓ Index iot-alertes: {initial_count} documents")
except Exception as e:
    print(f"❌ Erreur Elasticsearch: {e}")
    exit(1)

# Étape 3: Vérifier Redis avant upload
print(f"\n[3] État initial Redis...")
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    r.ping()
    queue_before = r.llen("iot:data")
    print(f"✓ Redis accessible")
    print(f"✓ Queue iot:data: {queue_before} messages")
except Exception as e:
    print(f"❌ Erreur Redis: {e}")
    exit(1)

# Étape 4: Upload via API Django (simulant Angular)
print(f"\n[4] Upload du fichier via API Django...")
try:
    with open(TEST_FILE, 'rb') as f:
        files = {'file': (TEST_FILE.name, f, 'application/json')}
        data = {'data_type': 'alertes'}
        
        print(f"  → POST {API_URL}")
        print(f"  → Type de données: alertes")
        
        start_time = time.time()
        response = requests.post(API_URL, files=files, data=data, timeout=30)
        upload_time = time.time() - start_time
        
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Upload réussi en {upload_time:.2f}s")
        print(f"  → Fichier: {result['filename']}")
        print(f"  → Type: {result['data_type']}")
        print(f"  → Enregistrements traités: {result['records_processed']}")
        print(f"  → Queue Redis: {result['redis_queue_length']} messages")
    else:
        print(f"❌ Upload échoué: {response.status_code}")
        print(f"   {response.text}")
        exit(1)
        
except Exception as e:
    print(f"❌ Erreur upload: {e}")
    exit(1)

# Étape 5: Vérifier Redis après upload
print(f"\n[5] Vérification Redis après upload...")
time.sleep(1)
queue_after_upload = r.llen("iot:data")
print(f"✓ Queue iot:data: {queue_after_upload} messages")

if queue_after_upload > queue_before:
    print(f"✓ {queue_after_upload - queue_before} nouveaux messages ajoutés")
else:
    print(f"⚠ Aucun nouveau message (probablement déjà consommé)")

# Étape 6: Attendre que Logstash traite les données
print(f"\n[6] Attente du traitement par Logstash...")
print("  Logstash consomme Redis et indexe dans Elasticsearch...")

for i in range(15):
    time.sleep(1)
    queue_len = r.llen("iot:data")
    
    if i % 3 == 0:
        print(f"  [{i+1}s] Queue Redis: {queue_len} messages", end="")
        
        if queue_len == 0:
            print(" ✓ (vide - traité!)")
            break
        else:
            print()

# Étape 7: Vérifier Elasticsearch après traitement
print(f"\n[7] Vérification Elasticsearch après traitement...")
time.sleep(2)  # Attendre l'indexation

try:
    # Rafraîchir l'index pour voir les nouveaux documents
    requests.post(f"{ES_URL}/iot-alertes/_refresh")
    
    # Compter tous les documents
    response = requests.get(f"{ES_URL}/iot-alertes/_count")
    final_count = response.json()['count']
    print(f"✓ Total documents: {final_count}")
    
    # Chercher les documents uploadés via Angular
    query = {
        "query": {
            "bool": {
                "must": [
                    {"exists": {"field": "source_file"}},
                    {"match": {"source_file": "test_angular_to_elasticsearch.json"}}
                ]
            }
        },
        "size": 0
    }
    
    response = requests.post(
        f"{ES_URL}/iot-alertes/_search",
        json=query,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        angular_docs = response.json()['hits']['total']['value']
        print(f"✓ Documents avec source_file 'test_angular_to_elasticsearch.json': {angular_docs}")
        
        if angular_docs > 0:
            # Récupérer un exemple
            query['size'] = 1
            response = requests.post(
                f"{ES_URL}/iot-alertes/_search",
                json=query,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.json()['hits']['hits']:
                doc = response.json()['hits']['hits'][0]['_source']
                print(f"\n✓ Exemple de document indexé:")
                print(f"  → ID: {doc.get('id_alerte')}")
                print(f"  → Type: {doc.get('type_alerte')}")
                print(f"  → Sévérité: {doc.get('severite')}")
                print(f"  → Source: {doc.get('source_file')}")
                print(f"  → Data Type: {doc.get('data_type')}")
                print(f"  → Upload Timestamp: {doc.get('upload_timestamp')}")
        
except Exception as e:
    print(f"❌ Erreur vérification: {e}")

# Résumé final
print(f"\n" + "="*80)
print("RÉSUMÉ DU TEST")
print("="*80)
print(f"📤 Upload Angular: ✓")
print(f"🔧 Traitement Django: ✓")
print(f"📦 Queue Redis: {queue_before} → {queue_after_upload} → {r.llen('iot:data')}")
print(f"⚙️  Traitement Logstash: {f'✓ ({queue_after_upload} messages traités)' if r.llen('iot:data') == 0 else '⚠ (en cours)'}")
print(f"🔍 Index Elasticsearch: {initial_count} → {final_count} documents")

if angular_docs > 0:
    print(f"\n🎉 SUCCÈS! Pipeline complet fonctionnel!")
    print(f"   Angular → Django → Redis → Logstash → Elasticsearch ✓")
    print(f"   {angular_docs} nouveaux documents indexés avec métadonnées")
else:
    print(f"\n⚠️  ATTENTION: Documents uploadés mais pas (encore) visibles dans ES")
    print(f"   Vérifiez les logs Logstash: docker-compose logs logstash")

print("="*80)
