#!/usr/bin/env python3
import json
import os

# Chemins des fichiers
input_dir = "/usr/share/logstash/input_files"
output_dir = "/usr/share/logstash/input_files/processed"

# Créer le dossier de sortie
os.makedirs(output_dir, exist_ok=True)

# Fichiers JSON array à convertir en NDJSON
json_files = [
    ("logs_alertes.json", "logs_alertes.ndjson"),
    ("logs_consommation.json", "logs_consommation.ndjson")
]

for input_file, output_file in json_files:
    input_path = os.path.join(input_dir, input_file)
    output_path = os.path.join(output_dir, output_file)
    
    if os.path.exists(input_path):
        print(f"Converting {input_file} to NDJSON format...")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for record in data:
                json.dump(record, f, ensure_ascii=False)
                f.write('\n')
        
        print(f"  ✓ Created {output_file} with {len(data)} records")
    else:
        print(f"  ✗ File not found: {input_path}")

print("\nConversion complete!")
