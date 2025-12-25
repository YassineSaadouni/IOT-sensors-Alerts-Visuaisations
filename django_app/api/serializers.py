"""
Serializers pour l'API REST
"""
from rest_framework import serializers
from .models import FileUploadHistory, ElasticsearchQuery


class FileUploadHistorySerializer(serializers.ModelSerializer):
    """Serializer pour l'historique des uploads"""
    
    class Meta:
        model = FileUploadHistory
        fields = '__all__'
        read_only_fields = ('uploaded_at',)


class FileUploadSerializer(serializers.Serializer):
    """Serializer pour l'upload de fichiers"""
    
    file = serializers.FileField()
    
    def validate_file(self, value):
        """Valider le fichier uploadé"""
        # Vérifier l'extension
        allowed_extensions = ['.csv', '.json']
        file_ext = value.name.lower().split('.')[-1]
        
        if f'.{file_ext}' not in allowed_extensions:
            raise serializers.ValidationError(
                f"Format de fichier non supporté. Formats acceptés: {', '.join(allowed_extensions)}"
            )
        
        # Vérifier la taille (max 16MB)
        max_size = 16 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                f"Fichier trop volumineux. Taille maximum: 16MB"
            )
        
        return value


class DeviceSerializer(serializers.Serializer):
    """Serializer générique pour les devices (depuis Elasticsearch)"""
    
    device_id = serializers.CharField(required=False)
    vehicle_id = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=False)
    source_file = serializers.CharField(required=False)
    file_type = serializers.CharField(required=False)
    upload_timestamp = serializers.DateTimeField(required=False)
    
    # Champs dynamiques (seront ajoutés selon les données)
    def to_representation(self, instance):
        """Représentation flexible pour gérer tous les champs Elasticsearch"""
        return instance


class SensorDataSerializer(serializers.Serializer):
    """Serializer pour les données de capteurs"""
    
    device_id = serializers.CharField()
    temperature = serializers.FloatField(required=False, allow_null=True)
    humidity = serializers.FloatField(required=False, allow_null=True)
    battery_level = serializers.IntegerField(required=False, allow_null=True)
    location = serializers.CharField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField(required=False)
    source_file = serializers.CharField(required=False)


class VehicleDataSerializer(serializers.Serializer):
    """Serializer pour les données de véhicules"""
    
    vehicle_id = serializers.CharField()
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    speed = serializers.FloatField(required=False, allow_null=True)
    fuel_level = serializers.IntegerField(required=False, allow_null=True)
    driver = serializers.CharField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)
    timestamp = serializers.DateTimeField(required=False)
    source_file = serializers.CharField(required=False)


class ElasticsearchQuerySerializer(serializers.ModelSerializer):
    """Serializer pour les requêtes Elasticsearch sauvegardées"""
    
    class Meta:
        model = ElasticsearchQuery
        fields = '__all__'
        read_only_fields = ('created_at',)


class SearchRequestSerializer(serializers.Serializer):
    """Serializer pour les requêtes de recherche"""
    
    query = serializers.CharField(required=False, allow_blank=True)
    index = serializers.CharField(required=False, allow_blank=True, default=None)
    size = serializers.IntegerField(required=False, default=50, min_value=1, max_value=10000)
    from_offset = serializers.IntegerField(required=False, default=0, min_value=0)
    
    # Filtres
    device_id = serializers.CharField(required=False, allow_blank=True)
    vehicle_id = serializers.CharField(required=False, allow_blank=True)
    source_file = serializers.CharField(required=False, allow_blank=True)
    file_type = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    
    # Date range
    date_from = serializers.DateTimeField(required=False, allow_null=True)
    date_to = serializers.DateTimeField(required=False, allow_null=True)
    
    # Sorting
    sort_by = serializers.CharField(required=False, default='@timestamp')
    sort_order = serializers.ChoiceField(
        choices=['asc', 'desc'],
        required=False,
        default='desc'
    )


class AggregationRequestSerializer(serializers.Serializer):
    """Serializer pour les requêtes d'agrégation"""
    
    index = serializers.CharField(required=False, allow_blank=True, default=None)
    field = serializers.CharField(required=True)
    agg_type = serializers.ChoiceField(
        choices=['terms', 'stats', 'date_histogram', 'range'],
        required=False,
        default='terms'
    )
    size = serializers.IntegerField(required=False, default=10, min_value=1, max_value=1000)
    
    # Pour date_histogram
    interval = serializers.CharField(required=False, default='1d')
    
    # Pour range
    ranges = serializers.ListField(required=False, allow_empty=True)
