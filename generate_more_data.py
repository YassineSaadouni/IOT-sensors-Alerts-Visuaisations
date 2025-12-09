#!/usr/bin/env python3
"""
Générateur de données IoT pour enrichir la base
Génère des données réalistes pour alimenter Kibana et Angular
"""

import json
import csv
import random
from datetime import datetime, timedelta

# Données de référence
BATIMENTS = ["Batiment A", "Batiment B", "Batiment C", "Batiment D"]
ZONES = ["Zone Nord", "Zone Sud", "Zone Est", "Zone Ouest", "Zone Centrale"]
TYPES_CAPTEURS = ["temperature", "humidite", "CO2", "luminosite", "pression", "qualite_air"]
TYPES_SALLES = ["conference", "bureau", "laboratoire", "salle_serveur", "open_space", "cafeteria"]
SEVERITES = ["faible", "moyenne", "haute", "critique"]
STATUTS = ["non_resolue", "en_cours", "resolue", "planifiee"]
TYPES_ENERGIE = ["electricite", "eau", "gaz"]
SOUS_TYPES_ENERGIE = ["climatisation", "chauffage", "eclairage", "equipements", "ascenseurs"]
TYPES_EQUIPEMENTS = ["CVC", "Ascenseur", "Eclairage", "Alarme", "Pompe", "Generateur"]
TYPES_MAINTENANCE = ["preventive", "corrective", "predictive"]

def generate_timestamp(days_ago=30):
    """Générer un timestamp aléatoire dans les N derniers jours"""
    now = datetime.now()
    past = now - timedelta(days=days_ago)
    random_date = past + (now - past) * random.random()
    return random_date.strftime('%Y-%m-%d %H:%M:%S')

def generate_alertes(count=50):
    """Générer des alertes"""
    alertes = []
    for i in range(count):
        alerte = {
            "id_alerte": f"ALT-{datetime.now().strftime('%Y%m%d')}-{i+6:03d}",
            "timestamp": generate_timestamp(7),
            "type_alerte": random.choice(["seuil_depasse", "anomalie_detectee", "panne_equipement", "batterie_faible"]),
            "categorie": random.choice(["qualite_air", "temperature", "humidite", "pression", "batterie", "climatisation"]),
            "severite": random.choice(SEVERITES),
            "priorite": random.choice(["P1", "P2", "P3", "P4"]),
            "capteur_id": f"CAP_{random.choice(TYPES_CAPTEURS).upper()}_{random.randint(1,50):03d}",
            "valeur_actuelle": round(random.uniform(15, 35), 1),
            "seuil": round(random.uniform(18, 25), 1),
            "duree_depassement": random.randint(5, 120),
            "description": f"Alerte générée automatiquement - {random.choice(['Seuil dépassé', 'Anomalie détectée', 'Vérification requise'])}",
            "batiment": random.choice(BATIMENTS),
            "salle": f"Salle {random.randint(1, 50)}",
            "etage": random.randint(0, 5),
            "zone": random.choice(ZONES),
            "technicien_assigné": f"TECH-{random.randint(1, 50):03d}",
            "statut": random.choice(STATUTS),
            "date_creation": generate_timestamp(7),
            "date_modification": generate_timestamp(3),
            "actions_requises": [random.choice(["Vérifier capteur", "Ajuster paramètres", "Remplacer composant"])],
            "impact": random.choice(["confort_utilisateurs", "securite", "economie_energie", "surveillance_temperature"]),
            "code_erreur": f"ERR_{random.randint(1000, 9999)}"
        }
        alertes.append(alerte)
    return alertes

def generate_capteurs(count=50):
    """Générer des données de capteurs"""
    capteurs = []
    for i in range(count):
        capteur = {
            "timestamp": generate_timestamp(7),
            "capteur_id": f"CAP_{random.randint(1000, 9999)}",
            "type": random.choice(TYPES_CAPTEURS),
            "valeur": round(random.uniform(18, 28), 2),
            "unite": random.choice(["°C", "%", "ppm", "lux", "hPa"]),
            "batiment": random.choice(BATIMENTS),
            "salle": f"Salle {random.randint(1, 50)}",
            "etage": random.randint(0, 5),
            "zone": random.choice(ZONES),
            "statut_capteur": random.choice(["actif", "inactif", "maintenance", "erreur"]),
            "batterie": round(random.uniform(20, 100), 1),
            "precision": round(random.uniform(0.1, 2.0), 2),
            "derniere_calibration": generate_timestamp(30),
            "seuil_min": round(random.uniform(15, 18), 1),
            "seuil_max": round(random.uniform(25, 30), 1)
        }
        capteurs.append(capteur)
    return capteurs

def generate_consommation(count=50):
    """Générer des données de consommation"""
    consommations = []
    for i in range(count):
        valeur = round(random.uniform(100, 5000), 2)
        cout_unitaire = round(random.uniform(0.10, 0.30), 3)
        conso = {
            "timestamp": generate_timestamp(30),
            "periode_mesure": random.choice(["heure", "jour", "semaine"]),
            "type_energie": random.choice(TYPES_ENERGIE),
            "sous_type": random.choice(SOUS_TYPES_ENERGIE),
            "valeur_consommation": valeur,
            "unite": random.choice(["kWh", "m³", "L"]),
            "batiment": random.choice(BATIMENTS),
            "zone": random.choice(ZONES),
            "equipement_id": f"EQP_{random.randint(1000, 9999)}",
            "cout_estime": round(valeur * cout_unitaire, 2),
            "cout_unitaire": cout_unitaire,
            "empreinte_carbone": round(valeur * random.uniform(0.05, 0.15), 2),
            "tendance": random.choice(["hausse", "baisse", "stable"]),
            "comparaison_mois_precedent": round(random.uniform(-20, 20), 1),
            "pointes_consommation": [f"{random.randint(8, 10)}h-{random.randint(11, 13)}h", f"{random.randint(14, 17)}h-{random.randint(18, 20)}h"],
            "facteur_charge": round(random.uniform(0.5, 0.95), 2)
        }
        consommations.append(conso)
    return consommations

def generate_occupation(count=50):
    """Générer des données d'occupation"""
    occupations = []
    for i in range(count):
        capacite = random.randint(10, 100)
        nombre_personnes = random.randint(0, capacite)
        occup = {
            "timestamp": generate_timestamp(7),
            "salle_id": f"SALLE_{random.randint(100, 999)}",
            "batiment": random.choice(BATIMENTS),
            "type_salle": random.choice(TYPES_SALLES),
            "capacite_max": capacite,
            "nombre_personnes": nombre_personnes,
            "taux_utilisation": round((nombre_personnes / capacite) * 100, 1),
            "evenement": random.choice(["Réunion", "Formation", "Conférence", "Workshop", ""]),
            "organisateur": f"ORG_{random.randint(1, 50):03d}" if random.random() > 0.3 else "",
            "duree_prevue": random.randint(30, 240),
            "equipements_utilises": random.choice(["Vidéoprojecteur", "Écrans", "Vidéoprojecteur, Écrans", "Aucun"]),
            "temperature_moyenne": round(random.uniform(19, 24), 1),
            "co2_moyen": random.randint(400, 1200),
            "consommation_elec": round(random.uniform(0.5, 5.0), 2),
            "statut_occupation": random.choice(["occupee", "libre", "reservee", "nettoyage"]),
            "zone": random.choice(ZONES),
            "etage": random.randint(0, 5)
        }
        occupations.append(occup)
    return occupations

def generate_maintenance(count=50):
    """Générer des données de maintenance"""
    maintenances = []
    for i in range(count):
        maint = {
            "timestamp": generate_timestamp(60),
            "intervention_id": f"INT-{datetime.now().strftime('%Y%m%d')}-{i+8:03d}",
            "equipement_id": f"EQP_{random.randint(1000, 9999)}",
            "type_equipement": random.choice(TYPES_EQUIPEMENTS),
            "marque": random.choice(["Siemens", "Schneider", "ABB", "Daikin", "Carrier", "Honeywell"]),
            "modele": f"MOD-{random.randint(100, 999)}",
            "type_maintenance": random.choice(TYPES_MAINTENANCE),
            "severite": random.choice(["faible", "moyenne", "critique"]),
            "vie_restante": random.randint(10, 90),
            "prediction_panne": random.choice(["faible", "moyen", "eleve"]),
            "cout_estime": round(random.uniform(500, 15000), 2),
            "technicien": f"TECH-{random.randint(1, 50):03d}",
            "batiment": random.choice(BATIMENTS),
            "salle": f"Salle {random.randint(1, 50)}",
            "zone": random.choice(ZONES),
            "description": f"Maintenance {random.choice(['préventive', 'corrective'])} programmée",
            "composants_affectes": random.choice(["compresseur", "moteur", "ventilateur", "pompe", "circuit"]),
            "historique_pannes": random.randint(0, 10),
            "duree_intervention_estimee": random.randint(1, 8),
            "pieces_requises": random.choice(["filtres", "joints", "courroies", "roulements", "aucune"])
        }
        maintenances.append(maint)
    return maintenances

def save_to_files():
    """Sauvegarder les données générées dans des fichiers"""
    print("🔧 Génération de nouvelles données IoT...")
    
    # Générer les données
    alertes = generate_alertes(50)
    capteurs = generate_capteurs(50)
    consommations = generate_consommation(50)
    occupations = generate_occupation(50)
    maintenances = generate_maintenance(50)
    
    # Sauvegarder en JSON
    with open('./Fichier_logs/logs_alertes_generated.json', 'w', encoding='utf-8') as f:
        json.dump(alertes, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(alertes)} alertes générées")
    
    with open('./Fichier_logs/logs_consommation_generated.json', 'w', encoding='utf-8') as f:
        json.dump(consommations, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(consommations)} consommations générées")
    
    # Sauvegarder en CSV
    with open('./Fichier_logs/logs_capteurs_generated.csv', 'w', newline='', encoding='utf-8') as f:
        if capteurs:
            writer = csv.DictWriter(f, fieldnames=capteurs[0].keys())
            writer.writeheader()
            writer.writerows(capteurs)
    print(f"✅ {len(capteurs)} capteurs générés")
    
    with open('./Fichier_logs/logs_occupation_generated.csv', 'w', newline='', encoding='utf-8') as f:
        if occupations:
            writer = csv.DictWriter(f, fieldnames=occupations[0].keys())
            writer.writeheader()
            writer.writerows(occupations)
    print(f"✅ {len(occupations)} occupations générées")
    
    with open('./Fichier_logs/logs_maintenance_generated.csv', 'w', newline='', encoding='utf-8') as f:
        if maintenances:
            writer = csv.DictWriter(f, fieldnames=maintenances[0].keys())
            writer.writeheader()
            writer.writerows(maintenances)
    print(f"✅ {len(maintenances)} maintenances générées")
    
    print(f"\n🎉 Total: {len(alertes) + len(capteurs) + len(consommations) + len(occupations) + len(maintenances)} documents générés")

if __name__ == "__main__":
    save_to_files()
