"""
Views et ViewSets pour l'API REST
"""
import logging
import json
import csv
import io
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

import redis
from django.conf import settings

from .models import FileUploadHistory, ElasticsearchQuery
from .serializers import (
    FileUploadHistorySerializer,
    FileUploadSerializer,
    DeviceSerializer,
    SensorDataSerializer,
    VehicleDataSerializer,
    ElasticsearchQuerySerializer,
    SearchRequestSerializer,
    AggregationRequestSerializer,
)
from .elasticsearch_service import ElasticsearchService

logger = logging.getLogger(__name__)

# Connexion Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

# Service Elasticsearch
es_service = ElasticsearchService()


class HealthCheckView(APIView):
    """Endpoint de santé pour vérifier les services"""
    
    def get(self, request):
        """Vérifier le statut de tous les services"""
        
        # Redis
        try:
            redis_client.ping()
            redis_status = 'connected'
        except Exception as e:
            redis_status = f'disconnected: {str(e)}'
        
        # Elasticsearch
        es_connected = es_service.check_connection()
        es_status = 'connected' if es_connected else 'disconnected'
        
        # Redis queue
        try:
            queue_length = redis_client.llen("iot:data")
        except:
            queue_length = None
        
        return Response({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'redis': redis_status,
                'elasticsearch': es_status,
                'redis_queue_length': queue_length
            }
        })


class FileUploadView(APIView):
    """Vue pour uploader des fichiers (legacy endpoint compatible avec l'ancienne API Flask)"""
    
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """Upload un fichier CSV ou JSON"""
        
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']
        filename = file.name
        file_type = 'json' if filename.endswith('.json') else 'csv'
        
        # Extraire le data_type depuis le POST ou le déduire du nom de fichier
        data_type = request.data.get('data_type', None)
        
        # Si pas de data_type, essayer de le déduire du nom de fichier
        if not data_type:
            filename_lower = filename.lower()
            if 'alerte' in filename_lower:
                data_type = 'alertes'
            elif 'capteur' in filename_lower or 'sensor' in filename_lower:
                data_type = 'capteurs'
            elif 'consommation' in filename_lower:
                data_type = 'consommation'
            elif 'occupation' in filename_lower:
                data_type = 'occupation'
            elif 'maintenance' in filename_lower:
                data_type = 'maintenance'
            else:
                data_type = 'unknown'
        
        logger.info(f"📁 Fichier reçu: {filename} [Type: {data_type}]")
        
        # Lire le contenu
        try:
            file_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response({
                'error': 'Erreur d\'encodage',
                'message': 'Le fichier doit être encodé en UTF-8'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parser le fichier
        try:
            if file_type == 'json':
                data = json.loads(file_content)
                if isinstance(data, dict):
                    data = [data]
            else:  # CSV
                csv_file = io.StringIO(file_content)
                reader = csv.DictReader(csv_file)
                data = list(reader)
        except Exception as e:
            return Response({
                'error': 'Erreur de parsing',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not data:
            return Response({
                'error': 'Fichier vide',
                'message': 'Aucune donnée trouvée'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Envoyer vers Redis
        try:
            count = 0
            for record in data:
                enriched_record = {
                    "source_file": filename,
                    "file_type": file_type,
                    "data_type": data_type,
                    "upload_timestamp": datetime.now().isoformat(),
                    "data": record
                }
                redis_client.lpush("iot:data", json.dumps(enriched_record))
                count += 1
            
            queue_length = redis_client.llen("iot:data")
            
            # Sauvegarder l'historique
            FileUploadHistory.objects.create(
                filename=filename,
                file_type=file_type,
                records_count=count,
                status='completed'
            )
            
            logger.info(f"✅ {count} enregistrements envoyés vers Redis depuis {filename}")
            
            return Response({
                'success': True,
                'message': 'Fichier traité avec succès',
                'filename': filename,
                'file_type': file_type,
                'data_type': data_type,
                'records_processed': count,
                'redis_queue_length': queue_length,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'envoi vers Redis: {e}")
            
            # Sauvegarder l'erreur
            FileUploadHistory.objects.create(
                filename=filename,
                file_type=file_type,
                records_count=0,
                status='failed',
                error_message=str(e)
            )
            
            return Response({
                'error': 'Erreur serveur',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileUploadViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer l'historique des uploads"""
    
    queryset = FileUploadHistory.objects.all()
    serializer_class = FileUploadHistorySerializer
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obtenir les uploads récents"""
        recent_uploads = self.queryset[:20]
        serializer = self.get_serializer(recent_uploads, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des uploads"""
        total = self.queryset.count()
        completed = self.queryset.filter(status='completed').count()
        failed = self.queryset.filter(status='failed').count()
        
        return Response({
            'total_uploads': total,
            'completed': completed,
            'failed': failed,
            'success_rate': (completed / total * 100) if total > 0 else 0
        })


class DeviceViewSet(viewsets.ViewSet):
    """ViewSet pour gérer tous les devices (Elasticsearch)"""
    
    def list(self, request):
        """Lister tous les devices"""
        serializer = SearchRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        params = serializer.validated_data
        result = es_service.search(
            query=params.get('query'),
            index=params.get('index'),
            size=params.get('size', 50),
            from_offset=params.get('from_offset', 0),
            filters={
                'device_id': params.get('device_id'),
                'vehicle_id': params.get('vehicle_id'),
                'source_file': params.get('source_file'),
                'file_type': params.get('file_type'),
                'status': params.get('status'),
                '@timestamp_from': params.get('date_from'),
                '@timestamp_to': params.get('date_to'),
            },
            sort_by=params.get('sort_by', '@timestamp'),
            sort_order=params.get('sort_order', 'desc')
        )
        
        return Response(result)
    
    def retrieve(self, request, pk=None):
        """Récupérer un device par ID"""
        index = request.query_params.get('index', es_service.default_index)
        document = es_service.get_by_id(pk, index)
        
        if document:
            return Response(document)
        else:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class SensorViewSet(viewsets.ViewSet):
    """ViewSet pour les données de capteurs"""
    
    def list(self, request):
        """Lister les données de capteurs"""
        # Filtrer uniquement les capteurs (ont device_id)
        filters = {
            'device_id': request.query_params.get('device_id'),
            'source_file': request.query_params.get('source_file'),
            'status': request.query_params.get('status'),
        }
        
        # Retirer les None
        filters = {k: v for k, v in filters.items() if v is not None}
        
        result = es_service.search(
            query=request.query_params.get('query'),
            filters=filters,
            size=int(request.query_params.get('size', 50))
        )
        
        # Filtrer pour ne garder que les documents avec device_id
        if result.get('documents'):
            result['documents'] = [
                doc for doc in result['documents']
                if 'device_id' in doc
            ]
            result['count'] = len(result['documents'])
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistiques sur les capteurs"""
        return Response({
            'by_device': es_service.aggregate('device_id', 'terms', size=100),
            'by_location': es_service.aggregate('location', 'terms', size=20),
            'by_status': es_service.aggregate('status', 'terms', size=10),
            'temperature_stats': es_service.aggregate('temperature', 'stats'),
            'humidity_stats': es_service.aggregate('humidity', 'stats'),
        })


class VehicleViewSet(viewsets.ViewSet):
    """ViewSet pour les données de véhicules"""
    
    def list(self, request):
        """Lister les données de véhicules"""
        filters = {
            'vehicle_id': request.query_params.get('vehicle_id'),
            'driver': request.query_params.get('driver'),
            'status': request.query_params.get('status'),
        }
        
        filters = {k: v for k, v in filters.items() if v is not None}
        
        result = es_service.search(
            query=request.query_params.get('query'),
            filters=filters,
            size=int(request.query_params.get('size', 50))
        )
        
        # Filtrer pour ne garder que les documents avec vehicle_id
        if result.get('documents'):
            result['documents'] = [
                doc for doc in result['documents']
                if 'vehicle_id' in doc
            ]
            result['count'] = len(result['documents'])
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Statistiques sur les véhicules"""
        return Response({
            'by_vehicle': es_service.aggregate('vehicle_id', 'terms', size=100),
            'by_driver': es_service.aggregate('driver', 'terms', size=50),
            'by_status': es_service.aggregate('status', 'terms', size=10),
            'speed_stats': es_service.aggregate('speed', 'stats'),
            'fuel_level_stats': es_service.aggregate('fuel_level', 'stats'),
        })


class ElasticsearchSearchView(APIView):
    """Vue pour effectuer des recherches personnalisées"""
    
    def post(self, request):
        """Effectuer une recherche avec filtres"""
        serializer = SearchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        params = serializer.validated_data
        result = es_service.search(
            query=params.get('query'),
            index=params.get('index'),
            size=params.get('size', 50),
            from_offset=params.get('from_offset', 0),
            filters={
                'device_id': params.get('device_id'),
                'vehicle_id': params.get('vehicle_id'),
                'source_file': params.get('source_file'),
                'file_type': params.get('file_type'),
                'status': params.get('status'),
                '@timestamp_from': params.get('date_from'),
                '@timestamp_to': params.get('date_to'),
            },
            sort_by=params.get('sort_by', '@timestamp'),
            sort_order=params.get('sort_order', 'desc')
        )
        
        return Response(result)


class AggregationsView(APIView):
    """Vue pour effectuer des agrégations"""
    
    def post(self, request):
        """Effectuer une agrégation"""
        serializer = AggregationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        params = serializer.validated_data
        result = es_service.aggregate(
            field=params['field'],
            agg_type=params.get('agg_type', 'terms'),
            index=params.get('index'),
            size=params.get('size', 10),
            interval=params.get('interval'),
            ranges=params.get('ranges')
        )
        
        return Response(result)


class StatisticsView(APIView):
    """Vue pour obtenir des statistiques globales"""
    
    def get(self, request):
        """Obtenir les statistiques"""
        index = request.query_params.get('index', es_service.default_index)
        stats = es_service.get_statistics(index)
        
        return Response(stats)


# === Vues pour les nouveaux types de données ===

class AlertesView(APIView):
    """Vue pour gérer les alertes"""
    
    def get(self, request):
        """Récupérer les alertes avec filtres"""
        result = es_service.search(
            query=request.query_params.get('q'),
            index='iot-alertes',
            size=int(request.query_params.get('size', 50)),
            from_offset=int(request.query_params.get('from', 0)),
            filters={
                'severite': request.query_params.get('severite'),
                'statut': request.query_params.get('statut'),
                'categorie': request.query_params.get('categorie'),
                'batiment': request.query_params.get('batiment'),
            },
            sort_by=request.query_params.get('sort_by', '@timestamp'),
            sort_order=request.query_params.get('sort_order', 'desc')
        )
        return Response(result)


class AlertesStatsView(APIView):
    """Statistiques des alertes"""
    
    def get(self, request):
        stats = es_service.get_alertes_statistics()
        return Response(stats)


class CapteursView(APIView):
    """Vue pour gérer les capteurs"""
    
    def get(self, request):
        """Récupérer les données des capteurs avec filtres"""
        result = es_service.search(
            query=request.query_params.get('q'),
            index='iot-capteurs',
            size=int(request.query_params.get('size', 50)),
            from_offset=int(request.query_params.get('from', 0)),
            filters={
                'type': request.query_params.get('type'),
                'statut_capteur': request.query_params.get('statut'),
                'batiment': request.query_params.get('batiment'),
                'zone': request.query_params.get('zone'),
            },
            sort_by=request.query_params.get('sort_by', '@timestamp'),
            sort_order=request.query_params.get('sort_order', 'desc')
        )
        return Response(result)


class CapteursStatsView(APIView):
    """Statistiques des capteurs"""
    
    def get(self, request):
        stats = es_service.get_capteurs_statistics()
        return Response(stats)


class ConsommationView(APIView):
    """Vue pour gérer la consommation d'énergie"""
    
    def get(self, request):
        """Récupérer les données de consommation avec filtres"""
        result = es_service.search(
            query=request.query_params.get('q'),
            index='iot-consommation',
            size=int(request.query_params.get('size', 50)),
            from_offset=int(request.query_params.get('from', 0)),
            filters={
                'type_energie': request.query_params.get('type_energie'),
                'sous_type': request.query_params.get('sous_type'),
                'batiment': request.query_params.get('batiment'),
                'zone': request.query_params.get('zone'),
            },
            sort_by=request.query_params.get('sort_by', '@timestamp'),
            sort_order=request.query_params.get('sort_order', 'desc')
        )
        return Response(result)


class ConsommationStatsView(APIView):
    """Statistiques de consommation"""
    
    def get(self, request):
        stats = es_service.get_consommation_statistics()
        return Response(stats)


class OccupationView(APIView):
    """Vue pour gérer l'occupation des salles"""
    
    def get(self, request):
        """Récupérer les données d'occupation avec filtres"""
        result = es_service.search(
            query=request.query_params.get('q'),
            index='iot-occupation',
            size=int(request.query_params.get('size', 50)),
            from_offset=int(request.query_params.get('from', 0)),
            filters={
                'type_salle': request.query_params.get('type_salle'),
                'statut_occupation': request.query_params.get('statut'),
                'batiment': request.query_params.get('batiment'),
                'zone': request.query_params.get('zone'),
            },
            sort_by=request.query_params.get('sort_by', '@timestamp'),
            sort_order=request.query_params.get('sort_order', 'desc')
        )
        return Response(result)


class OccupationStatsView(APIView):
    """Statistiques d'occupation"""
    
    def get(self, request):
        stats = es_service.get_occupation_statistics()
        return Response(stats)


class MaintenanceView(APIView):
    """Vue pour gérer la maintenance"""
    
    def get(self, request):
        """Récupérer les données de maintenance avec filtres"""
        result = es_service.search(
            query=request.query_params.get('q'),
            index='iot-maintenance',
            size=int(request.query_params.get('size', 50)),
            from_offset=int(request.query_params.get('from', 0)),
            filters={
                'type_equipement': request.query_params.get('type_equipement'),
                'type_maintenance': request.query_params.get('type_maintenance'),
                'severite': request.query_params.get('severite'),
                'batiment': request.query_params.get('batiment'),
            },
            sort_by=request.query_params.get('sort_by', '@timestamp'),
            sort_order=request.query_params.get('sort_order', 'desc')
        )
        return Response(result)


class MaintenanceStatsView(APIView):
    """Statistiques de maintenance"""
    
    def get(self, request):
        stats = es_service.get_maintenance_statistics()
        return Response(stats)
