#!/usr/bin/env python3
"""
Script d'ingestion complète des données IoT dans Elasticsearch
Ingère tous les fichiers de logs avec les noms de colonnes corrects
"""

import json
import csv
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import sys

# Configuration Elasticsearch
ES_HOST = "http://elasticsearch:9200"
es = Elasticsearch([ES_HOST])

def ingest_alertes():
    """Ingérer les données d'alertes"""
    print("📊 Ingestion des alertes...")
    
    with open('../Fichier_logs/logs_alertes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    actions = []
    for item in data:
        # Parser la date
        if 'timestamp' in item:
            try:
                dt = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')
                item['@timestamp'] = dt.isoformat()
            except:
                pass
        
        # Convertir les champs numériques
        if 'valeur_actuelle' in item:
            item['valeur_actuelle'] = float(item['valeur_actuelle'])
        if 'seuil' in item:
            item['seuil'] = float(item['seuil'])
        if 'duree_depassement' in item:
            item['duree_depassement'] = int(item['duree_depassement'])
        if 'etage' in item:
            item['etage'] = int(item['etage'])
        
        action = {
            "_index": "iot-alertes",
            "_source": item
        }
        actions.append(action)
    
    # Bulk insert
    success, failed = helpers.bulk(es, actions, stats_only=True)
    print(f"✅ Alertes: {success} documents insérés, {failed} erreurs")
    return success

def ingest_capteurs():
    """Ingérer les données des capteurs"""
    print("📊 Ingestion des capteurs...")
    
    with open('../Fichier_logs/logs_capteurs.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        actions = []
        
        for row in reader:
            # Parser la date
            if 'timestamp' in row:
                try:
                    dt = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                    row['@timestamp'] = dt.isoformat()
                except:
                    pass
            
            # Convertir les champs numériques
            try:
                if 'valeur' in row and row['valeur']:
                    row['valeur'] = float(row['valeur'])
                if 'batterie' in row and row['batterie']:
                    row['batterie'] = float(row['batterie'])
                if 'etage' in row and row['etage']:
                    row['etage'] = int(row['etage'])
                if 'precision' in row and row['precision']:
                    row['precision'] = float(row['precision'])
                if 'seuil_min' in row and row['seuil_min']:
                    row['seuil_min'] = float(row['seuil_min'])
                if 'seuil_max' in row and row['seuil_max']:
                    row['seuil_max'] = float(row['seuil_max'])
            except:
                pass
            
            action = {
                "_index": "iot-capteurs",
                "_source": row
            }
            actions.append(action)
        
        success, failed = helpers.bulk(es, actions, stats_only=True)
        print(f"✅ Capteurs: {success} documents insérés, {failed} erreurs")
        return success

def ingest_consommation():
    """Ingérer les données de consommation"""
    print("📊 Ingestion de la consommation...")
    
    with open('../Fichier_logs/logs_consommation.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    actions = []
    for item in data:
        # Parser la date
        if 'timestamp' in item:
            try:
                dt = datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')
                item['@timestamp'] = dt.isoformat()
            except:
                pass
        
        # Convertir les champs numériques
        try:
            if 'valeur_consommation' in item:
                item['valeur_consommation'] = float(item['valeur_consommation'])
            if 'cout_estime' in item:
                item['cout_estime'] = float(item['cout_estime'])
            if 'cout_unitaire' in item:
                item['cout_unitaire'] = float(item['cout_unitaire'])
            if 'empreinte_carbone' in item:
                item['empreinte_carbone'] = float(item['empreinte_carbone'])
            if 'comparaison_mois_precedent' in item:
                item['comparaison_mois_precedent'] = float(item['comparaison_mois_precedent'])
            if 'facteur_charge' in item:
                item['facteur_charge'] = float(item['facteur_charge'])
        except:
            pass
        
        action = {
            "_index": "iot-consommation",
            "_source": item
        }
        actions.append(action)
    
    success, failed = helpers.bulk(es, actions, stats_only=True)
    print(f"✅ Consommation: {success} documents insérés, {failed} erreurs")
    return success

def ingest_occupation():
    """Ingérer les données d'occupation"""
    print("📊 Ingestion de l'occupation...")
    
    with open('../Fichier_logs/logs_occupation.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        actions = []
        
        for row in reader:
            # Parser la date
            if 'timestamp' in row:
                try:
                    dt = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                    row['@timestamp'] = dt.isoformat()
                except:
                    pass
            
            # Convertir les champs numériques
            try:
                if 'capacite_max' in row and row['capacite_max']:
                    row['capacite_max'] = int(row['capacite_max'])
                if 'nombre_personnes' in row and row['nombre_personnes']:
                    row['nombre_personnes'] = int(row['nombre_personnes'])
                if 'taux_utilisation' in row and row['taux_utilisation']:
                    row['taux_utilisation'] = float(row['taux_utilisation'])
                if 'temperature_moyenne' in row and row['temperature_moyenne']:
                    row['temperature_moyenne'] = float(row['temperature_moyenne'])
                if 'co2_moyen' in row and row['co2_moyen']:
                    row['co2_moyen'] = int(row['co2_moyen'])
                if 'consommation_elec' in row and row['consommation_elec']:
                    row['consommation_elec'] = float(row['consommation_elec'])
                if 'etage' in row and row['etage']:
                    row['etage'] = int(row['etage'])
            except:
                pass
            
            action = {
                "_index": "iot-occupation",
                "_source": row
            }
            actions.append(action)
        
        success, failed = helpers.bulk(es, actions, stats_only=True)
        print(f"✅ Occupation: {success} documents insérés, {failed} erreurs")
        return success

def ingest_maintenance():
    """Ingérer les données de maintenance"""
    print("📊 Ingestion de la maintenance...")
    
    with open('../Fichier_logs/logs_maintenance.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        actions = []
        
        for row in reader:
            # Parser la date
            if 'timestamp' in row:
                try:
                    dt = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                    row['@timestamp'] = dt.isoformat()
                except:
                    pass
            
            # Convertir les champs numériques
            try:
                if 'vie_restante' in row and row['vie_restante']:
                    row['vie_restante'] = int(row['vie_restante'])
                if 'cout_estime' in row and row['cout_estime']:
                    row['cout_estime'] = float(row['cout_estime'])
                if 'duree_intervention_estimee' in row and row['duree_intervention_estimee']:
                    row['duree_intervention_estimee'] = int(row['duree_intervention_estimee'])
            except:
                pass
            
            action = {
                "_index": "iot-maintenance",
                "_source": row
            }
            actions.append(action)
        
        success, failed = helpers.bulk(es, actions, stats_only=True)
        print(f"✅ Maintenance: {success} documents insérés, {failed} erreurs")
        return success

def delete_all_indices():
    """Supprimer tous les indices IoT existants"""
    print("🗑️  Suppression des anciens indices...")
    indices = ['iot-alertes', 'iot-capteurs', 'iot-consommation', 'iot-occupation', 'iot-maintenance']
    
    for index in indices:
        if es.indices.exists(index=index):
            es.indices.delete(index=index)
            print(f"   Supprimé: {index}")

def create_index_patterns():
    """Créer les index patterns pour Kibana"""
    print("🔧 Création des index patterns Kibana...")
    
    # Cette partie sera gérée via l'API Kibana ou manuellement
    patterns = [
        'iot-alertes',
        'iot-capteurs',
        'iot-consommation',
        'iot-occupation',
        'iot-maintenance'
    ]
    
    print("   Index patterns à créer dans Kibana:")
    for pattern in patterns:
        print(f"   - {pattern}")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🚀 Ingestion des données IoT dans Elasticsearch")
    print("=" * 60)
    
    # Vérifier la connexion à Elasticsearch
    if not es.ping():
        print("❌ Impossible de se connecter à Elasticsearch")
        sys.exit(1)
    
    print("✅ Connexion à Elasticsearch réussie")
    print()
    
    # Supprimer les anciens indices
    delete_all_indices()
    print()
    
    # Ingérer toutes les données
    total = 0
    total += ingest_alertes()
    total += ingest_capteurs()
    total += ingest_consommation()
    total += ingest_occupation()
    total += ingest_maintenance()
    
    print()
    print("=" * 60)
    print(f"✨ Ingestion terminée: {total} documents au total")
    print("=" * 60)
    print()
    
    # Afficher les indices créés
    print("📊 Indices Elasticsearch:")
    indices_info = es.cat.indices(index='iot-*', v=True, format='json')
    for idx in indices_info:
        print(f"   {idx['index']}: {idx['docs.count']} documents ({idx['store.size']})")
    
    print()
    create_index_patterns()
    print()
    print("🎉 Prêt pour Kibana et Angular!")

if __name__ == "__main__":
    main()
