#!/usr/bin/env python3
"""
Debug Logstash - Injecter un message simple et tracer son chemin
"""

import redis
import json
from datetime import datetime
import time

r = redis.Redis(host='localhost', port=6379, password='redis_password_123', decode_responses=True)

# Message de test ultra-simple
test_message = {
    "source_file": "DEBUG_TEST.json",
    "file_type": "json",
    "data_type": "alertes",
    "upload_timestamp": datetime.now().isoformat(),
    "data": {
        "id_alerte": "ALT-DEBUG-SIMPLE",
        "timestamp": "2025-12-09T12:00:00Z",
        "type_alerte": "debug",
        "categorie": "test",
        "severite": "faible",
        "batiment": "Test",
        "salle": "Debug",
        "zone": "Test",
        "technicien_assigne": "Debug",
        "statut": "ouverte",
        "description": "Message de debug simple"
    }
}

print("Injection d'un message de test dans Redis...")
print(json.dumps(test_message, indent=2))

r.lpush("iot:data", json.dumps(test_message))

print(f"\n✓ Message injecté!")
print(f"Queue length: {r.llen('iot:data')}")

print("\nAttendez 10 secondes et surveillez:")
print("1. docker-compose logs --follow logstash")
print("2. Queue Redis: docker exec redis_container redis-cli -a redis_password_123 LLEN iot:data")
print("3. ES: curl http://localhost:9200/iot-alertes/_search?q=id_alerte:ALT-DEBUG-SIMPLE")
