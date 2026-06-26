# backend/api/views/admin_settings_views.py
"""
Vues pour les paramètres administrateur
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from ..models import User, AuditLog
from ..permissions import IsAdmin
from django.core.cache import cache


class AdminSettingsView(APIView):
    """
    GET /api/v1/admin/settings - Récupérer les paramètres
    PUT /api/v1/admin/settings - Mettre à jour les paramètres
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    # Clé de cache pour les paramètres
    SETTINGS_CACHE_KEY = 'admin_settings'

    def get_default_settings(self):
        """Paramètres par défaut"""
        return {
            'app_name': 'Suivi Grossesse',
            'contact_email': 'contact@suivi-grossesse.com',
            'session_timeout': 60,
            'max_attempts': 5,
            'notifications': {
                'email': True,
                'sms': False,
                'push': False
            }
        }

    @extend_schema(
        summary="Récupérer les paramètres",
        tags=["Administrateur"]
    )
    def get(self, request):
        try:
            # Essayer de récupérer depuis le cache
            settings = cache.get(self.SETTINGS_CACHE_KEY)
            
            if settings is None:
                # Si pas en cache, utiliser les paramètres par défaut
                settings = self.get_default_settings()
                # Sauvegarder en cache pour 1 heure
                cache.set(self.SETTINGS_CACHE_KEY, settings, 3600)
            
            return Response({
                'message': 'Paramètres récupérés.',
                'data': settings
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Erreur get settings: {e}")
            return Response({
                'message': 'Erreur lors de la récupération des paramètres.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Mettre à jour les paramètres",
        tags=["Administrateur"]
    )
    def put(self, request):
        try:
            settings = request.data
            
            # Validation de base
            if 'app_name' in settings and not settings['app_name']:
                return Response({
                    'message': 'Le nom de l\'application est requis.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if 'contact_email' in settings and not settings['contact_email']:
                return Response({
                    'message': 'L\'email de contact est requis.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Sauvegarder en cache
            cache.set(self.SETTINGS_CACHE_KEY, settings, 3600)
            
            # Journaliser l'action
            AuditLog.objects.create(
                user=request.user,
                action='ADMIN_UPDATE_SETTINGS',
                description=f"Administrateur {request.user.email} a mis à jour les paramètres",
                ip_address=self.get_client_ip(request),
            )
            
            return Response({
                'message': 'Paramètres mis à jour avec succès.',
                'data': settings
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Erreur update settings: {e}")
            return Response({
                'message': 'Erreur lors de la mise à jour des paramètres.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip