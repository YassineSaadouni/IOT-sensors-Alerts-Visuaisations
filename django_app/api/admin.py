"""
Admin configuration pour l'application API
"""
from django.contrib import admin
from .models import FileUploadHistory, ElasticsearchQuery


@admin.register(FileUploadHistory)
class FileUploadHistoryAdmin(admin.ModelAdmin):
    """Admin pour l'historique des uploads"""
    
    list_display = ('filename', 'file_type', 'records_count', 'status', 'uploaded_at')
    list_filter = ('file_type', 'status', 'uploaded_at')
    search_fields = ('filename',)
    readonly_fields = ('uploaded_at',)
    
    fieldsets = (
        ('Fichier', {
            'fields': ('filename', 'file_type', 'records_count')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Métadonnées', {
            'fields': ('uploaded_at',)
        }),
    )


@admin.register(ElasticsearchQuery)
class ElasticsearchQueryAdmin(admin.ModelAdmin):
    """Admin pour les requêtes sauvegardées"""
    
    list_display = ('name', 'index_name', 'is_favorite', 'created_at', 'created_by')
    list_filter = ('is_favorite', 'index_name', 'created_at')
    search_fields = ('name', 'description', 'created_by')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'description', 'created_by', 'is_favorite')
        }),
        ('Requête', {
            'fields': ('index_name', 'query_body')
        }),
        ('Métadonnées', {
            'fields': ('created_at',)
        }),
    )
