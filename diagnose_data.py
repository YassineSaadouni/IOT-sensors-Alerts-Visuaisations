#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnostic Elasticsearch - Verifier le contenu reel des documents
"""

from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['http://localhost:9200'], verify_certs=False, ssl_show_warn=False)

def check_index_sample(index_name, size=3):
    """Afficher des exemples de documents d'un index"""
    print(f"\n{'='*70}")
    print(f"INDEX: {index_name}")
    print('='*70)
    
    try:
        # Compter les documents
        count = es.count(index=index_name)['count']
        print(f"Total documents: {count}")
        
        # Recuperer des exemples
        result = es.search(index=index_name, size=size, body={
            "query": {"match_all": {}}
        })
        
        if result['hits']['hits']:
            print(f"\nExemples de documents:\n")
            for i, hit in enumerate(result['hits']['hits'], 1):
                print(f"--- Document {i} ---")
                source = hit['_source']
                
                # Afficher tous les champs
                if source:
                    for key, value in source.items():
                        print(f"  {key}: {value}")
                else:
                    print("  VIDE - Aucun champ!")
                print()
        else:
            print("Aucun document trouve!")
            
        # Afficher le mapping
        mapping = es.indices.get_mapping(index=index_name)
        print(f"\nMapping des champs:")
        props = mapping[index_name]['mappings'].get('properties', {})
        if props:
            for field, details in props.items():
                field_type = details.get('type', 'object')
                print(f"  - {field}: {field_type}")
        else:
            print("  Aucun champ mappe!")
            
    except Exception as e:
        print(f"Erreur: {e}")

def main():
    print("="*70)
    print("DIAGNOSTIC ELASTICSEARCH - CONTENU DES DOCUMENTS")
    print("="*70)
    
    # Verifier la connexion
    try:
        info = es.info()
        print(f"\nConnecte a Elasticsearch {info['version']['number']}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return
    
    # Verifier chaque index
    indices = ['iot-alertes', 'iot-capteurs', 'iot-consommation', 'iot-occupation', 'iot-maintenance']
    
    for index in indices:
        if es.indices.exists(index=index):
            check_index_sample(index, size=2)
        else:
            print(f"\n{index}: N'EXISTE PAS")
    
    print("\n" + "="*70)
    print("DIAGNOSTIC TERMINE")
    print("="*70)

if __name__ == "__main__":
    main()
