"""
URL configuration for BigData IoT Backend
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# Router pour les ViewSets
router = DefaultRouter()
router.register(r'devices', views.DeviceViewSet, basename='device')
router.register(r'sensors', views.SensorViewSet, basename='sensor')
router.register(r'vehicles', views.VehicleViewSet, basename='vehicle')
router.register(r'files', views.FileUploadViewSet, basename='file-upload')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(router.urls)),
    
    # Endpoints personnalisés
    path('api/search/', views.ElasticsearchSearchView.as_view(), name='elasticsearch-search'),
    path('api/stats/', views.StatisticsView.as_view(), name='statistics'),
    path('api/aggregations/', views.AggregationsView.as_view(), name='aggregations'),
    path('api/health/', views.HealthCheckView.as_view(), name='health-check'),
    
    # Nouveaux endpoints pour les fichiers logs
    path('api/alertes/', views.AlertesView.as_view(), name='alertes'),
    path('api/alertes/stats/', views.AlertesStatsView.as_view(), name='alertes-stats'),
    path('api/capteurs/', views.CapteursView.as_view(), name='capteurs'),
    path('api/capteurs/stats/', views.CapteursStatsView.as_view(), name='capteurs-stats'),
    path('api/consommation/', views.ConsommationView.as_view(), name='consommation'),
    path('api/consommation/stats/', views.ConsommationStatsView.as_view(), name='consommation-stats'),
    path('api/occupation/', views.OccupationView.as_view(), name='occupation'),
    path('api/occupation/stats/', views.OccupationStatsView.as_view(), name='occupation-stats'),
    path('api/maintenance/', views.MaintenanceView.as_view(), name='maintenance'),
    path('api/maintenance/stats/', views.MaintenanceStatsView.as_view(), name='maintenance-stats'),
    
    # Upload de fichiers (legacy endpoint)
    path('upload/', views.FileUploadView.as_view(), name='file-upload-legacy'),
]
