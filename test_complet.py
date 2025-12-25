#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    SCRIPT DE TEST COMPLET - Plateforme IoT Big Data
═══════════════════════════════════════════════════════════════════════════════

Ce script teste l'ensemble du pipeline de données :
    1. Services Docker (Elasticsearch, Redis, Logstash, Django, Angular)
    2. Upload de fichiers via API REST Django
    3. Traitement via Redis et Logstash
    4. Indexation dans Elasticsearch
    5. API de recherche et agrégations
    6. Interface Angular

Usage:
    python test_complet.py                    # Test complet
    python test_complet.py --quick            # Tests rapides uniquement
    python test_complet.py --services         # Tester uniquement les services
    python test_complet.py --upload           # Tester uniquement l'upload
    python test_complet.py --search           # Tester uniquement la recherche

Auteur: Projet Big Data IoT
Date: 2025
═══════════════════════════════════════════════════════════════════════════════
"""

import requests
import json
import time
import sys
import argparse
import redis
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

# URLs des services
API_URL = "http://localhost:8000"
ES_URL = "http://localhost:9200"
KIBANA_URL = "http://localhost:5601"
ANGULAR_URL = "http://localhost:4200"

# Configuration Redis
REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "password": "redis_password_123",
    "decode_responses": True
}

# Répertoire des fichiers de test
FICHIERS_DIR = Path("Fichier_logs")

# Configuration d'encodage Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Couleurs pour l'affichage (désactivées sur Windows)
USE_COLORS = sys.platform != 'win32'

# ═══════════════════════════════════════════════════════════════════════════
# UTILITAIRES D'AFFICHAGE
# ═══════════════════════════════════════════════════════════════════════════

class Colors:
    """Codes couleurs ANSI pour terminal"""
    if USE_COLORS:
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        MAGENTA = '\033[95m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
    else:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = RESET = BOLD = ''


def print_header(text: str) -> None:
    """Affiche un header principal"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═'*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═'*80}{Colors.RESET}\n")


def print_subheader(text: str) -> None:
    """Affiche un sous-header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.RESET}")


def print_success(text: str) -> None:
    """Affiche un message de succès"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str) -> None:
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text: str) -> None:
    """Affiche un message d'avertissement"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text: str) -> None:
    """Affiche un message d'information"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def print_result(name: str, success: bool, details: str = "") -> None:
    """Affiche le résultat d'un test"""
    status = f"{Colors.GREEN}PASS{Colors.RESET}" if success else f"{Colors.RED}FAIL{Colors.RESET}"
    print(f"  [{status}] {name}")
    if details:
        print(f"        {details}")


# ═══════════════════════════════════════════════════════════════════════════
# TESTS DES SERVICES
# ═══════════════════════════════════════════════════════════════════════════

def test_elasticsearch() -> Tuple[bool, str]:
    """Test de connexion à Elasticsearch"""
    try:
        response = requests.get(f"{ES_URL}", timeout=5)
        if response.status_code == 200:
            info = response.json()
            version = info.get('version', {}).get('number', 'unknown')
            return True, f"Version {version}"
        return False, f"Status code: {response.status_code}"
    except Exception as e:
        return False, str(e)


def test_kibana() -> Tuple[bool, str]:
    """Test de connexion à Kibana"""
    try:
        response = requests.get(f"{KIBANA_URL}/api/status", timeout=5)
        if response.status_code == 200:
            return True, "Kibana accessible"
        return False, f"Status code: {response.status_code}"
    except Exception as e:
        return False, str(e)


def test_redis() -> Tuple[bool, str]:
    """Test de connexion à Redis"""
    try:
        r = redis.Redis(**REDIS_CONFIG)
        r.ping()
        queue_length = r.llen("iot:data")
        return True, f"Queue: {queue_length} messages"
    except Exception as e:
        return False, str(e)


def test_django_api() -> Tuple[bool, str]:
    """Test de l'API Django"""
    try:
        response = requests.get(f"{API_URL}/api/health/", timeout=5)
        if response.status_code == 200:
            health = response.json()
            services = health.get('services', {})
            es_status = services.get('elasticsearch', 'unknown')
            redis_status = services.get('redis', 'unknown')
            return True, f"ES: {es_status}, Redis: {redis_status}"
        return False, f"Status code: {response.status_code}"
    except Exception as e:
        return False, str(e)


def test_angular() -> Tuple[bool, str]:
    """Test de l'application Angular"""
    try:
        response = requests.get(ANGULAR_URL, timeout=5)
        if response.status_code == 200:
            return True, "Application accessible"
        return False, f"Status code: {response.status_code}"
    except Exception as e:
        return False, str(e)


def run_service_tests() -> bool:
    """Exécute tous les tests de services"""
    print_header("TESTS DES SERVICES")
    
    tests = [
        ("Elasticsearch", test_elasticsearch),
        ("Kibana", test_kibana),
        ("Redis", test_redis),
        ("Django API", test_django_api),
        ("Angular Frontend", test_angular)
    ]
    
    results = []
    for name, test_func in tests:
        success, details = test_func()
        print_result(name, success, details)
        results.append(success)
    
    all_passed = all(results)
    print(f"\n{Colors.BOLD}Résultat: {len([r for r in results if r])}/{len(results)} services opérationnels{Colors.RESET}")
    return all_passed


# ═══════════════════════════════════════════════════════════════════════════
# TESTS D'UPLOAD
# ═══════════════════════════════════════════════════════════════════════════

def upload_file(filename: str, data_type: str) -> Tuple[bool, Dict]:
    """Upload un fichier vers l'API"""
    filepath = FICHIERS_DIR / filename
    
    if not filepath.exists():
        return False, {"error": f"Fichier non trouvé: {filepath}"}
    
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (filename, f)}
            data = {'data_type': data_type}
            response = requests.post(
                f"{API_URL}/upload/",
                files=files,
                data=data,
                timeout=30
            )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"Status {response.status_code}: {response.text}"}
            
    except Exception as e:
        return False, {"error": str(e)}


def test_upload_alertes() -> Tuple[bool, str]:
    """Test d'upload des alertes"""
    success, result = upload_file("test_alertes_upload.json", "alertes")
    if success:
        records = result.get('records_processed', 0)
        return True, f"{records} enregistrements traités"
    return False, result.get('error', 'Erreur inconnue')


def test_upload_capteurs() -> Tuple[bool, str]:
    """Test d'upload des données capteurs"""
    success, result = upload_file("logs_capteurs.csv", "capteurs")
    if success:
        records = result.get('records_processed', 0)
        return True, f"{records} enregistrements traités"
    return False, result.get('error', 'Erreur inconnue')


def test_upload_consommation() -> Tuple[bool, str]:
    """Test d'upload des données de consommation"""
    success, result = upload_file("test_consommation_energie.json", "consommation")
    if success:
        records = result.get('records_processed', 0)
        return True, f"{records} enregistrements traités"
    return False, result.get('error', 'Erreur inconnue')


def run_upload_tests() -> bool:
    """Exécute tous les tests d'upload"""
    print_header("TESTS D'UPLOAD DE FICHIERS")
    
    tests = [
        ("Upload Alertes (JSON)", test_upload_alertes),
        ("Upload Capteurs (CSV)", test_upload_capteurs),
        ("Upload Consommation (JSON)", test_upload_consommation)
    ]
    
    results = []
    for name, test_func in tests:
        success, details = test_func()
        print_result(name, success, details)
        results.append(success)
    
    all_passed = all(results)
    print(f"\n{Colors.BOLD}Résultat: {len([r for r in results if r])}/{len(results)} uploads réussis{Colors.RESET}")
    return all_passed


# ═══════════════════════════════════════════════════════════════════════════
# TESTS DE TRAITEMENT (REDIS → LOGSTASH → ELASTICSEARCH)
# ═══════════════════════════════════════════════════════════════════════════

def wait_for_processing(seconds: int = 10) -> None:
    """Attendre le traitement des données"""
    print_info(f"Attente de {seconds}s pour le traitement Logstash...")
    time.sleep(seconds)


def check_index_count(index: str) -> Tuple[bool, int]:
    """Vérifier le nombre de documents dans un index"""
    try:
        response = requests.get(f"{ES_URL}/{index}/_count", timeout=5)
        if response.status_code == 200:
            count = response.json()['count']
            return True, count
        return False, 0
    except Exception as e:
        return False, 0


def test_elasticsearch_indexation() -> Tuple[bool, str]:
    """Test de l'indexation dans Elasticsearch"""
    indices = ['iot-alertes', 'iot-capteurs', 'iot-consommation', 'iot-occupation', 'iot-maintenance']
    
    total_docs = 0
    failed = []
    
    for index in indices:
        success, count = check_index_count(index)
        if success:
            total_docs += count
        else:
            failed.append(index)
    
    if failed:
        return False, f"Échec pour: {', '.join(failed)}"
    
    return True, f"{total_docs} documents indexés sur {len(indices)} indices"


def run_processing_tests() -> bool:
    """Exécute les tests de traitement"""
    print_header("TESTS DE TRAITEMENT DES DONNÉES")
    
    # Attendre que Logstash traite les données uploadées
    wait_for_processing(15)
    
    success, details = test_elasticsearch_indexation()
    print_result("Indexation Elasticsearch", success, details)
    
    return success


# ═══════════════════════════════════════════════════════════════════════════
# TESTS DE RECHERCHE ET AGRÉGATIONS
# ═══════════════════════════════════════════════════════════════════════════

def test_search_api() -> Tuple[bool, str]:
    """Test de l'API de recherche"""
    try:
        payload = {
            "query": "batiment",
            "size": 10
        }
        response = requests.post(
            f"{API_URL}/api/search/",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            total = result.get('total', 0)
            return True, f"{total} résultats trouvés"
        return False, f"Status {response.status_code}"
        
    except Exception as e:
        return False, str(e)


def test_aggregations_api() -> Tuple[bool, str]:
    """Test de l'API d'agrégations"""
    try:
        payload = {
            "aggs": {
                "by_type": {
                    "terms": {
                        "field": "data_type.keyword"
                    }
                }
            }
        }
        response = requests.post(
            f"{API_URL}/api/aggregations/",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            buckets = result.get('aggregations', {}).get('by_type', {}).get('buckets', [])
            return True, f"{len(buckets)} types de données"
        return False, f"Status {response.status_code}"
        
    except Exception as e:
        return False, str(e)


def test_statistics_api() -> Tuple[bool, str]:
    """Test de l'API de statistiques"""
    try:
        response = requests.get(f"{API_URL}/api/statistics/", timeout=10)
        
        if response.status_code == 200:
            stats = response.json()
            total = stats.get('total_documents', 0)
            return True, f"{total} documents au total"
        return False, f"Status {response.status_code}"
        
    except Exception as e:
        return False, str(e)


def run_search_tests() -> bool:
    """Exécute les tests de recherche"""
    print_header("TESTS DE RECHERCHE ET AGRÉGATIONS")
    
    tests = [
        ("Recherche texte", test_search_api),
        ("Agrégations", test_aggregations_api),
        ("Statistiques", test_statistics_api)
    ]
    
    results = []
    for name, test_func in tests:
        success, details = test_func()
        print_result(name, success, details)
        results.append(success)
    
    all_passed = all(results)
    print(f"\n{Colors.BOLD}Résultat: {len([r for r in results if r])}/{len(results)} tests réussis{Colors.RESET}")
    return all_passed


# ═══════════════════════════════════════════════════════════════════════════
# FONCTION PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Tests complets de la plateforme IoT Big Data")
    parser.add_argument('--quick', action='store_true', help='Tests rapides uniquement')
    parser.add_argument('--services', action='store_true', help='Tester uniquement les services')
    parser.add_argument('--upload', action='store_true', help='Tester uniquement l\'upload')
    parser.add_argument('--search', action='store_true', help='Tester uniquement la recherche')
    args = parser.parse_args()
    
    print_header("TESTS COMPLETS - PLATEFORME IOT BIG DATA")
    print_info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Tests des services (toujours exécutés en premier)
    if args.services or not (args.upload or args.search):
        results['services'] = run_service_tests()
        if not results['services']:
            print_error("\n❌ Les services ne sont pas tous opérationnels!")
            print_warning("Vérifiez avec: docker-compose ps")
            return 1
    
    # Tests d'upload
    if args.upload or (not args.quick and not args.services and not args.search):
        results['upload'] = run_upload_tests()
    
    # Tests de traitement
    if not args.quick and not args.services and not args.search:
        results['processing'] = run_processing_tests()
    
    # Tests de recherche
    if args.search or (not args.quick and not args.services and not args.upload):
        results['search'] = run_search_tests()
    
    # Résumé final
    print_header("RÉSUMÉ DES TESTS")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    
    for category, result in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if result else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"  {status} - {category.upper()}")
    
    print(f"\n{Colors.BOLD}Résultat global: {passed_tests}/{total_tests} catégories réussies{Colors.RESET}")
    
    if passed_tests == total_tests:
        print_success("\n🎉 Tous les tests sont passés avec succès!")
        return 0
    else:
        print_error(f"\n❌ {total_tests - passed_tests} catégorie(s) en échec")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠ Tests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
