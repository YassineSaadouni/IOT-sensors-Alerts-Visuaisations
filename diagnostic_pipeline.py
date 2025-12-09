#!/usr/bin/env python3
"""
Script de diagnostic du pipeline Redis → Logstash → Elasticsearch
"""

import redis
import json
import requests
from datetime import datetime

# Configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'redis_password_123'
ES_URL = 'http://localhost:9200'

print("="*60)
print("DIAGNOSTIC DU PIPELINE")
print("="*60)

# 1. Test Redis
print("\n[1] Connexion Redis...")
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    r.ping()
    print("✓ Redis accessible")
    
    # Longueur de la queue
    queue_len = r.llen("iot:data")
    print(f"✓ Queue iot:data: {queue_len} messages")
    
    # Lire un message si présent
    if queue_len > 0:
        message = r.lindex("iot:data", 0)
        print("\n  Premier message dans la queue:")
        data = json.loads(message)
        print(f"    source_file: {data.get('source_file')}")
        print(f"    data_type: {data.get('data_type')}")
        print(f"    file_type: {data.get('file_type')}")
        
except Exception as e:
    print(f"✗ Erreur Redis: {e}")

# 2. Test Elasticsearch
print("\n[2] Connexion Elasticsearch...")
try:
    response = requests.get(f"{ES_URL}/_cluster/health")
    if response.status_code == 200:
        health = response.json()
        print(f"✓ Elasticsearch accessible")
        print(f"✓ Status: {health['status']}")
        print(f"✓ Nodes: {health['number_of_nodes']}")
except Exception as e:
    print(f"✗ Erreur Elasticsearch: {e}")

# 3. Compter les documents dans les index
print("\n[3] Documents dans les index...")
indices = ['iot-alertes', 'iot-capteurs', 'iot-consommation', 'iot-occupation', 'iot-maintenance']
for idx in indices:
    try:
        response = requests.get(f"{ES_URL}/{idx}/_count")
        if response.status_code == 200:
            count = response.json()['count']
            print(f"  {idx}: {count} documents")
        else:
            print(f"  {idx}: index introuvable")
    except:
        print(f"  {idx}: erreur")

# 4. Chercher des documents uploadés via API
print("\n[4] Recherche de documents avec source_file...")
for idx in indices:
    try:
        query = {
            "query": {
                "exists": {
                    "field": "source_file"
                }
            },
            "size": 0
        }
        response = requests.post(
            f"{ES_URL}/{idx}/_search",
            json=query,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            count = response.json()['hits']['total']['value']
            if count > 0:
                print(f"  {idx}: {count} documents avec source_file ✓")
            else:
                print(f"  {idx}: 0 documents avec source_file")
    except:
        pass

# 5. Test injection manuelle dans Redis
print("\n[5] Test injection manuelle dans Redis...")
test_data = {
    "source_file": "diagnostic_test.json",
    "file_type": "json",
    "data_type": "alertes",
    "upload_timestamp": datetime.now().isoformat(),
    "data": {
        "id_alerte": "ALT-DIAG-001",
        "timestamp": "2025-12-09T10:00:00Z",
        "type_alerte": "test_diagnostic",
        "categorie": "test",
        "severite": "faible",
        "batiment": "Test",
        "salle": "Diagnostic",
        "zone": "Test",
        "technicien_assigne": "Auto",
        "statut": "ouverte",
        "description": "Test diagnostic du pipeline"
    }
}

try:
    r.lpush("iot:data", json.dumps(test_data))
    print("✓ Message de test injecté dans Redis")
    print(f"  Queue length: {r.llen('iot:data')}")
except Exception as e:
    print(f"✗ Erreur injection: {e}")

print("\n" + "="*60)
print("Attendez 10 secondes puis vérifiez si le message a été traité...")
print("="*60)
