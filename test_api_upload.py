"""
Script de test complet pour l'API d'upload de fichiers
Teste tous les endpoints d'upload avec differents types de fichiers
"""

import requests
import json
import time
import sys
import os
from pathlib import Path

# Configuration de l'encodage pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configuration
API_BASE_URL = "http://localhost:8000/api"
FICHIERS_DIR = Path("Fichier_logs")

# Couleurs pour l'affichage (desactivees sur Windows pour compatibilite)
USE_COLORS = sys.platform != 'win32'

class Colors:
    if USE_COLORS:
        GREEN = '\033[92m'
        RED = '\033[91m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
    else:
        GREEN = ''
        RED = ''
        YELLOW = ''
        BLUE = ''
        CYAN = ''
        RESET = ''
        BOLD = ''

def print_header(text):
    """Affiche un header stylisé"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Affiche un message de succes"""
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")

def print_error(text):
    """Affiche un message d'erreur"""
    print(f"{Colors.RED}[ERREUR] {text}{Colors.RESET}")

def print_info(text):
    """Affiche un message d'information"""
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")

def print_warning(text):
    """Affiche un message d'avertissement"""
    print(f"{Colors.YELLOW}[ATTENTION] {text}{Colors.RESET}")

def test_api_health():
    """Test de santé de l'API"""
    print_header("TEST 1: Santé de l'API")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print_success(f"API accessible - Status: {response.status_code}")
            return True
        else:
            print_error(f"API retourne un status incorrect: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Impossible de se connecter à l'API Django")
        print_warning("Vérifiez que Django est démarré: docker-compose ps")
        return False
    except Exception as e:
        print_error(f"Erreur lors du test de santé: {e}")
        return False

def test_upload_alertes():
    """Test d'upload du fichier alertes"""
    print_header("TEST 2: Upload Alertes (JSON)")
    
    fichier_path = FICHIERS_DIR / "test_alertes_upload.json"
    
    if not fichier_path.exists():
        print_error(f"Fichier non trouvé: {fichier_path}")
        return False
    
    print_info(f"Upload du fichier: {fichier_path.name}")
    
    try:
        with open(fichier_path, 'rb') as f:
            files = {'file': (fichier_path.name, f, 'application/json')}
            data = {'data_type': 'alertes'}
            start_time = time.time()
            response = requests.post(
                f"{API_BASE_URL.replace('/api', '')}/upload/",
                files=files,
                data=data,
                timeout=30
            )
            duration = time.time() - start_time
        
        print_info(f"Temps de réponse: {duration:.2f}s")
        print_info(f"Status code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_success(f"Upload réussi!")
            print_info(f"Réponse: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Échec de l'upload - Status: {response.status_code}")
            print_error(f"Réponse: {response.text}")
            return False
            
    except FileNotFoundError:
        print_error(f"Fichier non trouvé: {fichier_path}")
        return False
    except Exception as e:
        print_error(f"Erreur lors de l'upload: {e}")
        return False

def test_upload_alertes_critiques():
    """Test d'upload des alertes critiques"""
    print_header("TEST 3: Upload Alertes Critiques (JSON)")
    
    fichier_path = FICHIERS_DIR / "test_alertes_critiques.json"
    
    if not fichier_path.exists():
        print_error(f"Fichier non trouvé: {fichier_path}")
        return False
    
    print_info(f"Upload du fichier: {fichier_path.name}")
    
    try:
        with open(fichier_path, 'rb') as f:
            files = {'file': (fichier_path.name, f, 'application/json')}
            data = {'data_type': 'alertes'}
            start_time = time.time()
            response = requests.post(
                f"{API_BASE_URL.replace('/api', '')}/upload/",
                files=files,
                data=data,
                timeout=30
            )
            duration = time.time() - start_time
        
        print_info(f"Temps de réponse: {duration:.2f}s")
        print_info(f"Status code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_success(f"Upload réussi!")
            print_info(f"Réponse: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Échec de l'upload - Status: {response.status_code}")
            print_error(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Erreur lors de l'upload: {e}")
        return False

def test_upload_logs_csv():
    """Test d'upload d'un fichier CSV existant"""
    print_header("TEST 4: Upload Logs CSV")
    
    fichier_path = FICHIERS_DIR / "logs_occupation.csv"
    
    if not fichier_path.exists():
        print_warning(f"Fichier non trouvé: {fichier_path}")
        print_info("Test ignoré (fichier optionnel)")
        return None
    
    print_info(f"Upload du fichier: {fichier_path.name}")
    
    try:
        with open(fichier_path, 'rb') as f:
            files = {'file': (fichier_path.name, f, 'text/csv')}
            data = {'data_type': 'occupation'}
            start_time = time.time()
            response = requests.post(
                f"{API_BASE_URL.replace('/api', '')}/upload/",
                files=files,
                data=data,
                timeout=30
            )
            duration = time.time() - start_time
        
        print_info(f"Temps de réponse: {duration:.2f}s")
        print_info(f"Status code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print_success(f"Upload CSV réussi!")
            return True
        else:
            print_warning(f"Upload CSV échoué - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur lors de l'upload CSV: {e}")
        return False

def test_create_alerte_single():
    """Test de creation d'une alerte unique via POST - Note: endpoint read-only"""
    print_header("TEST 5: Creation d'une alerte unique")
    
    print_warning("Note: L'endpoint /api/alertes/ est en lecture seule (GET)")
    print_info("Pour ajouter des donnees, utilisez l'upload de fichiers ou ingest_all.py")
    
    # Ce test est informatif - l'endpoint n'accepte pas POST
    return None

def test_get_alertes_stats():
    """Test de récupération des statistiques d'alertes"""
    print_header("TEST 6: Récupération des statistiques")
    
    try:
        start_time = time.time()
        response = requests.get(
            f"{API_BASE_URL}/alertes/stats/",
            timeout=10
        )
        duration = time.time() - start_time
        
        print_info(f"Temps de réponse: {duration:.2f}s")
        print_info(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Statistiques récupérées!")
            print_info(f"Total d'alertes: {data.get('total', 'N/A')}")
            
            if 'by_severity' in data:
                print_info("\nRépartition par sévérité:")
                for item in data['by_severity']:
                    print(f"  - {item.get('severite', 'N/A')}: {item.get('count', 0)}")
            
            return True
        else:
            print_error(f"Échec de récupération - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur lors de la récupération: {e}")
        return False

def test_invalid_file():
    """Test d'upload d'un fichier invalide"""
    print_header("TEST 7: Upload fichier invalide (test negatif)")
    
    print_info("Creation d'un fichier JSON invalide temporaire")
    
    try:
        invalid_data = "{ invalid json content"
        
        files = {'file': ('invalid.json', invalid_data, 'application/json')}
        data = {'data_type': 'alertes'}
        response = requests.post(
            f"{API_BASE_URL.replace('/api', '')}/upload/",
            files=files,
            data=data,
            timeout=10
        )
        
        print_info(f"Status code: {response.status_code}")
        
        if response.status_code >= 400:
            print_success("L'API rejette correctement les fichiers invalides")
            print_info(f"Message d'erreur: {response.text}")
            return True
        else:
            print_warning("L'API accepte un fichier invalide (à vérifier)")
            return False
            
    except Exception as e:
        print_error(f"Erreur lors du test: {e}")
        return False

def test_large_batch():
    """Test d'upload d'un lot important d'alertes"""
    print_header("TEST 8: Upload lot important (performance)")
    
    print_info("Generation de 50 alertes de test")
    
    alertes = []
    for i in range(50):
        alertes.append({
            "id_alerte": f"ALT-BATCH-{int(time.time())}-{i}",
            "timestamp": "2025-12-09T12:00:00Z",
            "type_alerte": "test_batch",
            "categorie": "technique",
            "severite": "faible",
            "batiment": "Batiment Batch",
            "salle": f"Salle {i}",
            "zone": "Zone Batch",
            "technicien_assigne": "Testeur Batch",
            "statut": "ouverte",
            "description": f"Alerte batch #{i} pour test de performance"
        })
    
    try:
        # Creer un fichier temporaire JSON
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(alertes, f)
            temp_path = f.name
        
        print_info(f"Upload de {len(alertes)} alertes...")
        
        with open(temp_path, 'rb') as f:
            files = {'file': ('batch_test.json', f, 'application/json')}
            data = {'data_type': 'alertes'}
            start_time = time.time()
            response = requests.post(
                f"{API_BASE_URL.replace('/api', '')}/upload/",
                files=files,
                data=data,
                timeout=60
            )
            duration = time.time() - start_time
        
        # Nettoyer le fichier temporaire
        Path(temp_path).unlink()
        
        print_info(f"Temps de traitement: {duration:.2f}s")
        print_info(f"Vitesse: {len(alertes)/duration:.1f} alertes/seconde")
        print_info(f"Status code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print_success(f"Batch de {len(alertes)} alertes traité avec succès!")
            return True
        else:
            print_error(f"Échec du batch - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erreur lors du test batch: {e}")
        return False

def print_summary(results):
    """Affiche le résumé des tests"""
    print_header("RÉSUMÉ DES TESTS")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"\n{Colors.BOLD}Tests executes: {total}{Colors.RESET}")
    print(f"{Colors.GREEN}[OK] Reussis: {passed}{Colors.RESET}")
    print(f"{Colors.RED}[KO] Echoues: {failed}{Colors.RESET}")
    print(f"{Colors.YELLOW}[--] Ignores: {skipped}{Colors.RESET}")
    
    success_rate = (passed / (total - skipped) * 100) if (total - skipped) > 0 else 0
    print(f"\n{Colors.BOLD}Taux de reussite: {success_rate:.1f}%{Colors.RESET}")
    
    print("\n" + "="*60)
    print(f"{Colors.BOLD}Details des tests:{Colors.RESET}")
    for test_name, result in results.items():
        if result is True:
            print(f"{Colors.GREEN}[OK]{Colors.RESET} {test_name}")
        elif result is False:
            print(f"{Colors.RED}[ECHEC]{Colors.RESET} {test_name}")
        else:
            print(f"{Colors.YELLOW}[IGNORE]{Colors.RESET} {test_name}")
    print("="*60 + "\n")
    
    if failed > 0:
        print(f"{Colors.RED}{Colors.BOLD}[!] Certains tests ont echoue!{Colors.RESET}")
        print_info("Verifiez les logs ci-dessus pour plus de details")
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}[OK] Tous les tests ont reussi!{Colors.RESET}")

def main():
    """Fonction principale"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("=" * 60)
    print("     TEST COMPLET DE L'API D'UPLOAD - PROJET IOT")
    print("     Teste tous les endpoints d'upload et creation")
    print("=" * 60)
    print(f"{Colors.RESET}\n")
    
    print_info(f"API URL: {API_BASE_URL}")
    print_info(f"Dossier des fichiers: {FICHIERS_DIR}")
    print_info("Démarrage des tests...\n")
    
    time.sleep(1)
    
    # Dictionnaire pour stocker les résultats
    results = {}
    
    # Exécuter tous les tests
    results["1. Santé API"] = test_api_health()
    
    if not results["1. Santé API"]:
        print_error("\n⚠ L'API n'est pas accessible. Arrêt des tests.")
        print_info("Lancez Django avec: docker-compose up -d django")
        return
    
    time.sleep(0.5)
    results["2. Upload Alertes JSON"] = test_upload_alertes()
    
    time.sleep(0.5)
    results["3. Upload Alertes Critiques"] = test_upload_alertes_critiques()
    
    time.sleep(0.5)
    results["4. Upload Logs CSV"] = test_upload_logs_csv()
    
    time.sleep(0.5)
    results["5. Création Alerte Unique"] = test_create_alerte_single()
    
    time.sleep(0.5)
    results["6. Statistiques Alertes"] = test_get_alertes_stats()
    
    time.sleep(0.5)
    results["7. Fichier Invalide"] = test_invalid_file()
    
    time.sleep(0.5)
    results["8. Batch Performance"] = test_large_batch()
    
    # Afficher le résumé
    print_summary(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrompus par l'utilisateur{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Erreur fatale: {e}{Colors.RESET}")
