"""
Models pour l'application API
Utilise Elasticsearch comme source de données principale
"""
from django.db import models


class FileUploadHistory(models.Model):
    """Historique des fichiers uploadés"""
    
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=[('csv', 'CSV'), ('json', 'JSON')])
    records_count = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'file_upload_history'
        ordering = ['-uploaded_at']
        verbose_name = 'File Upload'
        verbose_name_plural = 'File Uploads'
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"


class ElasticsearchQuery(models.Model):
    """Sauvegarde des requêtes Elasticsearch populaires"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    query_body = models.JSONField()
    index_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True)
    is_favorite = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'elasticsearch_queries'
        ordering = ['-created_at']
        verbose_name = 'Elasticsearch Query'
        verbose_name_plural = 'Elasticsearch Queries'
    
    def __str__(self):
        return self.name
