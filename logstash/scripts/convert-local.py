import json

# Convertir logs_alertes.json
with open('../../Fichier_logs/logs_alertes.json', 'r', encoding='utf-8') as f:
    alertes = json.load(f)

with open('../../Fichier_logs/logs_alertes.ndjson', 'w', encoding='utf-8') as f:
    for record in alertes:
        json.dump(record, f, ensure_ascii=False)
        f.write('\n')

print(f"✓ Converted logs_alertes.json: {len(alertes)} records")

# Convertir logs_consommation.json
with open('../../Fichier_logs/logs_consommation.json', 'r', encoding='utf-8') as f:
    consommation = json.load(f)

with open('../../Fichier_logs/logs_consommation.ndjson', 'w', encoding='utf-8') as f:
    for record in consommation:
        json.dump(record, f, ensure_ascii=False)
        f.write('\n')

print(f"✓ Converted logs_consommation.json: {len(consommation)} records")
