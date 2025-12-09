#!/usr/bin/env python3
"""
Script de test complet du pipeline Upload API → Redis → Logstash → Elasticsearch
Test tous les types de données IoT et vérifie leur indexation
"""

import requests
import json
import time
import sys
from pathlib import Path
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
ES_BASE_URL = "http://localhost:9200"
FICHIERS_DIR = Path("Fichier_logs")

# Couleurs Windows-compatibles
USE_COLORS = sys.platform != 'win32'

def colored(text, color_code):
    if USE_COLORS:
        return f"\033[{color_code}m{text}\033[0m"
    return text

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    print(colored(f"[OK] {text}", "92"))

def print_error(text):
    print(colored(f"[ERREUR] {text}", "91"))

def print_warning(text):
    print(colored(f"[ATTENTION] {text}", "93"))

def print_info(text):
    print(colored(f"[INFO] {text}", "94"))


def upload_file(filename, data_type):
    """Upload un fichier vers l'API"""
    filepath = FICHIERS_DIR / filename
    
    if not filepath.exists():
        print_error(f"Fichier non trouvé: {filepath}")
        return None
    
    print_info(f"Upload: {filename} [Type: {data_type}]")
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (filename, f, 'application/json')}
            data = {'data_type': data_type}
            response = requests.post(
                f"{API_BASE_URL}/upload/",
                files=files,
                data=data,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"Upload réussi: {result['records_processed']} enregistrements")
            print_info(f"Queue Redis: {result['redis_queue_length']} messages")
            return result
        else:
            print_error(f"Échec: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Erreur: {e}")
        return None


def wait_for_logstash(seconds=10):
    """Attendre que Logstash traite les données"""
    print_info(f"Attente de {seconds}s pour le traitement Logstash...")
    for i in range(seconds):
        time.sleep(1)
        if i % 2 == 0:
            print(".", end="", flush=True)
    print(" OK")


def check_elasticsearch_count(index):
    """Vérifier le nombre de documents dans un index"""
    try:
        response = requests.get(f"{ES_BASE_URL}/{index}/_count", timeout=5)
        if response.status_code == 200:
            count = response.json()['count']
            return count
        return None
    except Exception as e:
        print_error(f"Erreur lors de la vérification de {index}: {e}")
        return None


def check_recent_documents(index, field, value):
    """Chercher des documents récents avec un champ spécifique"""
    try:
        query = {
            "query": {
                "exists": {
                    "field": field
                }
            },
            "size": 1,
            "sort": [
                {"upload_timestamp": {"order": "desc"}}
            ]
        }
        
        response = requests.post(
            f"{ES_BASE_URL}/{index}/_search",
            json=query,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            hits = response.json()['hits']['hits']
            if hits:
                doc = hits[0]['_source']
                return doc
        return None
    except Exception as e:
        return None


def test_pipeline_complet():
    """Test complet du pipeline"""
    
    print_header("TEST COMPLET DU PIPELINE IOT")
    print_info(f"API: {API_BASE_URL}")
    print_info(f"Elasticsearch: {ES_BASE_URL}")
    print_info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Liste des tests à effectuer
    tests = [
        {
            'filename': 'test_alertes_upload.json',
            'data_type': 'alertes',
            'index': 'iot-alertes',
            'check_field': 'source_file'
        },
        {
            'filename': 'test_capteurs_iot.json',
            'data_type': 'capteurs',
            'index': 'iot-capteurs',
            'check_field': 'source_file'
        },
        {
            'filename': 'test_consommation_energie.json',
            'data_type': 'consommation',
            'index': 'iot-consommation',
            'check_field': 'source_file'
        },
        {
            'filename': 'logs_occupation.csv',
            'data_type': 'occupation',
            'index': 'iot-occupation',
            'check_field': 'source_file'
        }
    ]
    
    results = []
    
    # Phase 1: Compter les documents avant upload
    print_header("PHASE 1: État initial Elasticsearch")
    initial_counts = {}
    for test in tests:
        count = check_elasticsearch_count(test['index'])
        initial_counts[test['index']] = count
        print_info(f"{test['index']}: {count} documents")
    
    # Phase 2: Upload des fichiers
    print_header("PHASE 2: Upload des fichiers")
    uploads_success = []
    for test in tests:
        result = upload_file(test['filename'], test['data_type'])
        uploads_success.append(result is not None)
        if result:
            test['uploaded_count'] = result['records_processed']
        time.sleep(1)
    
    # Phase 3: Attendre Logstash
    print_header("PHASE 3: Traitement Logstash")
    wait_for_logstash(15)
    
    # Phase 4: Vérifier Elasticsearch
    print_header("PHASE 4: Vérification Elasticsearch")
    for i, test in enumerate(tests):
        if not uploads_success[i]:
            print_warning(f"Skip {test['index']} (upload échoué)")
            continue
        
        # Compter les documents après
        final_count = check_elasticsearch_count(test['index'])
        initial = initial_counts.get(test['index'], 0)
        
        print_info(f"\n{test['index']}:")
        print_info(f"  Avant: {initial} documents")
        print_info(f"  Après: {final_count} documents")
        print_info(f"  Uploadé: {test.get('uploaded_count', 0)} enregistrements")
        
        # Chercher un document récent avec source_file
        recent_doc = check_recent_documents(test['index'], test['check_field'], test['filename'])
        
        if recent_doc:
            print_success(f"  Document récent trouvé avec source_file!")
            print_info(f"    source_file: {recent_doc.get('source_file')}")
            print_info(f"    data_type: {recent_doc.get('data_type')}")
            print_info(f"    upload_timestamp: {recent_doc.get('upload_timestamp')}")
            results.append(True)
        else:
            print_warning(f"  Aucun document récent avec {test['check_field']}")
            results.append(False)
    
    # Résumé final
    print_header("RÉSUMÉ FINAL")
    success_count = sum(results)
    total_count = len(results)
    
    print_info(f"Tests réussis: {success_count}/{total_count}")
    
    if success_count == total_count:
        print_success("\nTOUS LES TESTS RÉUSSIS! Pipeline opérationnel! 🎉")
        return 0
    elif success_count > 0:
        print_warning(f"\n{success_count} tests réussis sur {total_count}")
        return 1
    else:
        print_error("\nTOUS LES TESTS ONT ÉCHOUÉ!")
        return 2


if __name__ == '__main__':
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    exit_code = test_pipeline_complet()
    sys.exit(exit_code)
