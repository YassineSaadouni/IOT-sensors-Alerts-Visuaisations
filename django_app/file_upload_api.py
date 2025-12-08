"""
Flask API pour recevoir des fichiers (CSV/JSON) et les envoyer vers Redis
Les données sont ensuite consommées par Logstash pour indexation dans Elasticsearch
"""

from flask import Flask, request, jsonify
import redis
import json
import csv
import io
from datetime import datetime
import logging

# Configuration de l'application Flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite 16MB

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connexion Redis
redis_client = redis.Redis(
    host='redis',
    port=6379,
    password='redis_password_123',
    decode_responses=True
)

# Vérifier la connexion Redis au démarrage
try:
    redis_client.ping()
    logger.info("✅ Connexion Redis réussie")
except Exception as e:
    logger.error(f"❌ Erreur connexion Redis: {e}")


def process_json_file(file_content):
    """Traite un fichier JSON et retourne une liste de dictionnaires"""
    try:
        data = json.loads(file_content)
        
        # Si c'est un objet unique, le mettre dans une liste
        if isinstance(data, dict):
            data = [data]
        
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Erreur de parsing JSON: {str(e)}"


def process_csv_file(file_content):
    """Traite un fichier CSV et retourne une liste de dictionnaires"""
    try:
        csv_file = io.StringIO(file_content)
        reader = csv.DictReader(csv_file)
        data = list(reader)
        return data, None
    except Exception as e:
        return None, f"Erreur de parsing CSV: {str(e)}"


def send_to_redis(data_list, file_type, filename):
    """Envoie les données vers Redis avec métadonnées"""
    count = 0
    for record in data_list:
        # Enrichir chaque enregistrement avec des métadonnées
        enriched_record = {
            "source_file": filename,
            "file_type": file_type,
            "upload_timestamp": datetime.now().isoformat(),
            "data": record
        }
        
        # Envoyer vers Redis (liste iot:data)
        redis_client.lpush("iot:data", json.dumps(enriched_record))
        count += 1
    
    return count


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de santé pour vérifier que l'API fonctionne"""
    try:
        redis_client.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"
    
    return jsonify({
        "status": "healthy",
        "redis": redis_status,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint principal pour uploader des fichiers CSV ou JSON
    
    Usage:
        curl -X POST -F "file=@data.csv" http://localhost:8000/upload
        curl -X POST -F "file=@data.json" http://localhost:8000/upload
    """
    
    # Vérifier qu'un fichier est présent
    if 'file' not in request.files:
        return jsonify({
            "error": "Aucun fichier trouvé dans la requête",
            "message": "Utilisez le champ 'file' pour envoyer un fichier"
        }), 400
    
    file = request.files['file']
    
    # Vérifier que le fichier a un nom
    if file.filename == '':
        return jsonify({
            "error": "Nom de fichier vide",
            "message": "Le fichier doit avoir un nom"
        }), 400
    
    filename = file.filename
    logger.info(f"📁 Fichier reçu: {filename}")
    
    # Lire le contenu du fichier
    try:
        file_content = file.read().decode('utf-8')
    except UnicodeDecodeError:
        return jsonify({
            "error": "Erreur d'encodage",
            "message": "Le fichier doit être encodé en UTF-8"
        }), 400
    
    # Détecter le type de fichier et le traiter
    data_list = None
    error_msg = None
    
    if filename.endswith('.json'):
        data_list, error_msg = process_json_file(file_content)
        file_type = "json"
    elif filename.endswith('.csv'):
        data_list, error_msg = process_csv_file(file_content)
        file_type = "csv"
    else:
        return jsonify({
            "error": "Type de fichier non supporté",
            "message": "Seuls les fichiers .json et .csv sont acceptés",
            "filename": filename
        }), 400
    
    # Vérifier les erreurs de parsing
    if error_msg:
        return jsonify({
            "error": "Erreur de traitement",
            "message": error_msg,
            "filename": filename
        }), 400
    
    # Vérifier que des données ont été trouvées
    if not data_list or len(data_list) == 0:
        return jsonify({
            "error": "Fichier vide",
            "message": "Aucune donnée trouvée dans le fichier",
            "filename": filename
        }), 400
    
    # Envoyer les données vers Redis
    try:
        count = send_to_redis(data_list, file_type, filename)
        
        # Vérifier la longueur de la file Redis
        queue_length = redis_client.llen("iot:data")
        
        logger.info(f"✅ {count} enregistrements envoyés vers Redis depuis {filename}")
        
        return jsonify({
            "success": True,
            "message": f"Fichier traité avec succès",
            "filename": filename,
            "file_type": file_type,
            "records_processed": count,
            "redis_queue_length": queue_length,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'envoi vers Redis: {e}")
        return jsonify({
            "error": "Erreur serveur",
            "message": f"Impossible d'envoyer les données vers Redis: {str(e)}",
            "filename": filename
        }), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Obtenir des statistiques sur la file Redis"""
    try:
        queue_length = redis_client.llen("iot:data")
        
        return jsonify({
            "redis_queue_length": queue_length,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "error": "Erreur lors de la récupération des stats",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
