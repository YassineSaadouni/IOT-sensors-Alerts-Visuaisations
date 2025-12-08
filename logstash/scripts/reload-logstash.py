#!/usr/bin/env python3
"""
Script pour forcer le reload de tous les fichiers dans Logstash
en supprimant les fichiers sincedb
"""
import subprocess
import time

# Supprimer les indices existants
indices = [
    "iot-alertes",
    "iot-capteurs",
    "iot-consommation",
    "iot-occupation",
    "iot-maintenance"
]

for index in indices:
    try:
        subprocess.run(
            f"curl -X DELETE http://localhost:9200/{index}",
            shell=True,
            check=False
        )
        print(f"Deleted index: {index}")
    except Exception as e:
        print(f"Error deleting {index}: {e}")

# Supprimer les fichiers sincedb
subprocess.run(
    "docker exec logstash_container rm -rf /usr/share/logstash/sincedb/*",
    shell=True
)
print("Deleted sincedb files")

# Redémarrer Logstash
subprocess.run("docker restart logstash_container", shell=True)
print("Restarted Logstash")

# Attendre que Logstash démarre
print("Waiting 40 seconds for Logstash to start...")
time.sleep(40)

# Vérifier les indices
result = subprocess.run(
    "curl -s http://localhost:9200/_cat/indices?v",
    shell=True,
    capture_output=True,
    text=True
)
print("\nElasticsearch Indices:")
print(result.stdout)
