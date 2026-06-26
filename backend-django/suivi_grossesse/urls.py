"""
URL configuration du projet SuiviGrossesse
"""

from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # ================================================================
    #  DOCUMENTATION SWAGGER UI (drf-spectacular)
    # ================================================================
    # Schéma OpenAPI (JSON) - Généré automatiquement
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Interface Swagger UI - Interface interactive
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # ================================================================
    #  ROUTES DE L'API
    # ================================================================
    path('api/v1/', include('api.urls')),
]