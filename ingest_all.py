#!/usr/bin/env python3
"""
Script d'ingestion complète - Version simplifiée et fonctionnelle
"""

import json
import csv
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import sys
import os
import glob

ES_HOST = "http://localhost:9200"
es = Elasticsearch([ES_HOST], verify_certs=False, ssl_show_warn=False)
BASE_PATH = "./Fichier_logs"

def load_json_files(pattern):
    """Charger plusieurs fichiers JSON"""
    all_data = []
    files = glob.glob(f"{BASE_PATH}/{pattern}")
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data if isinstance(data, list) else [data])
                print(f"   Chargé: {os.path.basename(filepath)} ({len(data)} docs)")
        except Exception as e:
            print(f"   Erreur {filepath}: {e}")
    return all_data

def load_csv_files(pattern):
    """Charger plusieurs fichiers CSV"""
    all_data = []
    files = glob.glob(f"{BASE_PATH}/{pattern}")
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                all_data.extend(rows)
                print(f"   Chargé: {os.path.basename(filepath)} ({len(rows)} docs)")
        except Exception as e:
            print(f"   Erreur {filepath}: {e}")
    return all_data

def prepare_numeric_fields(data, int_fields=[], float_fields=[]):
    """Convertir les champs numériques"""
    for item in data:
        for field in int_fields:
            if field in item and item[field] and item[field] != 'NA':
                try:
                    item[field] = int(item[field])
                except:
                    pass
        for field in float_fields:
            if field in item and item[field] and item[field] != 'NA':
                try:
                    item[field] = float(item[field])
                except:
                    pass
        # Parser timestamp
        if 'timestamp' in item:
            try:
                dt = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')
                item['@timestamp'] = dt.isoformat()
            except:
                pass
    return data

def ingest_data(index_name, data):
    """Ingérer des données dans un index"""
    if not data:
        print(f"   Aucune donnée pour {index_name}")
        return 0
    
    actions = [{"_index": index_name, "_source": item} for item in data]
    try:
        success, errors = helpers.bulk(es, actions, stats_only=False, raise_on_error=False)
        if errors:
            print(f"   ⚠️  Quelques erreurs d'ingestion ({len(errors)} docs)")
        return len(actions) if isinstance(success, list) else success
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return 0

def main():
    print("=" * 70)
    print("🚀 Ingestion complète des données IoT")
    print("=" * 70)
    
    # Connexion
    try:
        info = es.info()
        print(f"✅ Connecté à Elasticsearch {info['version']['number']}\n")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        sys.exit(1)
    
    # Supprimer anciens indices
    print("🗑️  Suppression des anciens indices...")
    for idx in ['iot-alertes', 'iot-capteurs', 'iot-consommation', 'iot-occupation', 'iot-maintenance']:
        if es.indices.exists(index=idx):
            es.indices.delete(index=idx)
            print(f"   Supprimé: {idx}")
    print()
    
    total = 0
    
    # Alertes
    print("📊 ALERTES")
    data = load_json_files("logs_alertes*.json")
    data = prepare_numeric_fields(data, 
        int_fields=['duree_depassement', 'etage'],
        float_fields=['valeur_actuelle', 'seuil'])
    count = ingest_data('iot-alertes', data)
    print(f"✅ {count} alertes ingérées\n")
    total += count
    
    # Capteurs
    print("📊 CAPTEURS")
    data = load_csv_files("logs_capteurs*.csv")
    data = prepare_numeric_fields(data,
        int_fields=['etage'],
        float_fields=['valeur', 'batterie', 'precision', 'seuil_min', 'seuil_max'])
    count = ingest_data('iot-capteurs', data)
    print(f"✅ {count} capteurs ingérés\n")
    total += count
    
    # Consommation
    print("📊 CONSOMMATION")
    data = load_json_files("logs_consommation*.json")
    data = prepare_numeric_fields(data,
        float_fields=['valeur_consommation', 'cout_estime', 'cout_unitaire', 
                     'empreinte_carbone', 'comparaison_mois_precedent', 'facteur_charge'])
    count = ingest_data('iot-consommation', data)
    print(f"✅ {count} consommations ingérées\n")
    total += count
    
    # Occupation
    print("📊 OCCUPATION")
    data = load_csv_files("logs_occupation*.csv")
    data = prepare_numeric_fields(data,
        int_fields=['capacite_max', 'nombre_personnes', 'co2_moyen', 'etage'],
        float_fields=['taux_utilisation', 'temperature_moyenne', 'consommation_elec'])
    count = ingest_data('iot-occupation', data)
    print(f"✅ {count} occupations ingérées\n")
    total += count
    
    # Maintenance
    print("📊 MAINTENANCE")
    data = load_csv_files("logs_maintenance*.csv")
    data = prepare_numeric_fields(data,
        int_fields=['vie_restante', 'duree_intervention_estimee', 'historique_pannes'],
        float_fields=['cout_estime'])
    count = ingest_data('iot-maintenance', data)
    print(f"✅ {count} maintenances ingérées\n")
    total += count
    
    # Résumé
    print("=" * 70)
    print(f"✨ TOTAL: {total} documents ingérés")
    print("=" * 70)
    print()
    
    # Attendre le refresh
    print("⏳ Attente du refresh Elasticsearch...")
    import time
    time.sleep(2)
    
    # Afficher les indices
    print("📊 INDICES CRÉÉS:")
    try:
        indices = es.cat.indices(index='iot-*', v=True, format='json')
        for idx in indices:
            print(f"   • {idx['index']:<20} {idx['docs.count']:>6} documents  ({idx['store.size']})")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    print()
    print("🎉 Prêt pour Kibana et Angular!")
    print()
    print("📌 Étapes suivantes:")
    print("   1. Ouvrir Kibana: http://localhost:5601")
    print("   2. Créer index pattern: iot-*")
    print("   3. Explorer les données dans Discover")
    print("   4. Créer des dashboards")
    print("   5. Tester les API Django")

if __name__ == "__main__":
    main()
