"""
Vues pour les ADMINISTRATEURS
Gestion des utilisateurs, supervision, statistiques, logs
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from datetime import datetime, timedelta

from ..models import (
    User, Pregnancy, Appointment, Consultation, 
    MedicalExam, VitalSign, Alert, FollowUpSchedule, AuditLog, UserCaregiver
)
from ..serializers import (
    UserPublicSerializer, RegisterSerializer,
    PregnancySerializer, AppointmentSerializer,
    ConsultationSerializer, MedicalExamSerializer,
    VitalSignSerializer, AlertSerializer
)
from ..permissions import IsAdmin


# ============================================================
# 1. GESTION DES UTILISATEURS
# ============================================================

class AdminUserListView(APIView):
    """
    GET /api/v1/admin/users - Liste de tous les utilisateurs
    POST /api/v1/admin/users - Créer un utilisateur (admin)
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @extend_schema(
        summary="Liste des utilisateurs",
        description="Récupère tous les utilisateurs de la plateforme.",
        responses={200: UserPublicSerializer(many=True)},
        tags=["Administrateur"]
    )
    def get(self, request):
        users = User.objects.all().order_by('-created_at')
        return Response({
            'message': 'Liste des utilisateurs.',
            'data': UserPublicSerializer(users, many=True).data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Créer un utilisateur",
        description="Crée un nouvel utilisateur avec le rôle spécifié.",
        request=RegisterSerializer,
        responses={201: UserPublicSerializer},
        tags=["Administrateur"]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        user = serializer.save()
        
        # Journaliser l'action
        AuditLog.objects.create(
            user=request.user,
            action='ADMIN_CREATE_USER',
            description=f"Administrateur {request.user.email} a créé l'utilisateur {user.email}",
        )
        
        return Response({
            'message': 'Utilisateur créé avec succès.',
            'data': UserPublicSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class AdminUserDetailView(APIView):
    """
    GET /api/v1/admin/users/<id> - Détail d'un utilisateur
    PUT /api/v1/admin/users/<id> - Modifier un utilisateur
    DELETE /api/v1/admin/users/<id> - Désactiver/supprimer un utilisateur
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    
    @extend_schema(
        summary="Détail d'un utilisateur",
        description="Récupère les détails d'un utilisateur spécifique.",
        responses={200: UserPublicSerializer, 404: OpenApiResponse(description="Utilisateur non trouvé")},
        tags=["Administrateur"]
    )
    def get(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response({
                'message': 'Utilisateur non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'message': 'Détail de l\'utilisateur.',
            'data': UserPublicSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Modifier un utilisateur",
        description="Modifie les informations d'un utilisateur.",
        request=RegisterSerializer,
        responses={200: UserPublicSerializer},
        tags=["Administrateur"]
    )
    def put(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response({
                'message': 'Utilisateur non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Ne pas permettre de modifier son propre rôle pour éviter les abus
        if user.id == request.user.id and request.data.get('role'):
            return Response({
                'message': 'Vous ne pouvez pas modifier votre propre rôle.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        validated_data = serializer.validated_data
        
        # Mettre à jour les champs
        for key, value in validated_data.items():
            if key != 'password' and key != 'password_confirmation':
                setattr(user, key, value)
        
        if 'password' in validated_data and validated_data['password']:
            user.set_password(validated_data['password'])
        
        user.save()
        
        return Response({
            'message': 'Utilisateur mis à jour.',
            'data': UserPublicSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Désactiver un utilisateur",
        description="Désactive un utilisateur (compte non supprimé mais désactivé).",
        responses={200: OpenApiResponse(description="Utilisateur désactivé")},
        tags=["Administrateur"]
    )
    def delete(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response({
                'message': 'Utilisateur non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Ne pas permettre de désactiver son propre compte
        if user.id == request.user.id:
            return Response({
                'message': 'Vous ne pouvez pas désactiver votre propre compte.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = False
        user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='ADMIN_DEACTIVATE_USER',
            description=f"Administrateur {request.user.email} a désactivé l'utilisateur {user.email}",
        )
        
        return Response({
            'message': f'Utilisateur {user.username} désactivé avec succès.'
        }, status=status.HTTP_200_OK)


class AdminUserRoleView(APIView):
    """
    PUT /api/v1/admin/users/<id>/role - Changer le rôle d'un utilisateur
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @extend_schema(
        summary="Changer le rôle d'un utilisateur",
        description="""
        Change le rôle d'un utilisateur.
        
        Rôles disponibles :
        - PATIENTE : Patiente
        - SOIGNANT : Soignant (sage-femme, gynécologue)
        - ADMIN : Administrateur
        """,
        request={
            "type": "object",
            "properties": {
                "role": {
                    "type": "string",
                    "enum": ["PATIENTE", "SOIGNANT", "ADMIN"]
                }
            },
            "required": ["role"]
        },
        responses={200: UserPublicSerializer},
        tags=["Administrateur"]
    )
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({
                'message': 'Utilisateur non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Ne pas permettre de modifier son propre rôle
        if user.id == request.user.id:
            return Response({
                'message': 'Vous ne pouvez pas modifier votre propre rôle.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        new_role = request.data.get('role')
        if new_role not in ['PATIENTE', 'SOIGNANT', 'ADMIN']:
            return Response({
                'message': 'Rôle invalide. Utilisez PATIENTE, SOIGNANT ou ADMIN.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        old_role = user.role
        user.role = new_role
        user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='ADMIN_CHANGE_ROLE',
            description=f"Administrateur {request.user.email} a changé le rôle de {user.email} de {old_role} à {new_role}",
        )
        
        return Response({
            'message': f'Rôle de {user.username} changé de {old_role} à {new_role}.',
            'data': UserPublicSerializer(user).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 2. STATISTIQUES ET SUPERVISION
# ============================================================

class AdminStatsView(APIView):
    """
    GET /api/v1/admin/stats - Statistiques de la plateforme
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @extend_schema(
        summary="Statistiques de la plateforme",
        description="Récupère les statistiques générales de la plateforme.",
        responses={
            200: OpenApiResponse(
                description="Statistiques récupérées",
                response={
                    "type": "object",
                    "properties": {
                        "total_users": {"type": "integer"},
                        "total_patients": {"type": "integer"},
                        "total_caregivers": {"type": "integer"},
                        "total_admins": {"type": "integer"},
                        "total_pregnancies": {"type": "integer"},
                        "active_pregnancies": {"type": "integer"},
                        "total_appointments": {"type": "integer"},
                        "pending_appointments": {"type": "integer"},
                        "completed_appointments": {"type": "integer"},
                        "total_consultations": {"type": "integer"},
                        "total_exams": {"type": "integer"},
                        "total_alerts": {"type": "integer"},
                        "active_alerts": {"type": "integer"},
                        "critical_alerts": {"type": "integer"}
                    }
                }
            )
        },
        tags=["Administrateur"]
    )
    def get(self, request):
        # Statistiques utilisateurs
        total_users = User.objects.count()
        total_patients = User.objects.filter(role='PATIENTE').count()
        total_caregivers = User.objects.filter(role='SOIGNANT').count()
        total_admins = User.objects.filter(role='ADMIN').count()
        
        # Statistiques grossesses
        total_pregnancies = Pregnancy.objects.count()
        active_pregnancies = Pregnancy.objects.filter(is_active=True).count()
        
        # Statistiques rendez-vous
        total_appointments = Appointment.objects.count()
        pending_appointments = Appointment.objects.filter(
            status__in=['SCHEDULED', 'CONFIRMED']
        ).count()
        completed_appointments = Appointment.objects.filter(status='COMPLETED').count()
        
        # Statistiques consultations et examens
        total_consultations = Consultation.objects.count()
        total_exams = MedicalExam.objects.count()
        
        # Statistiques alertes
        total_alerts = Alert.objects.count()
        active_alerts = Alert.objects.filter(status='ACTIVE').count()
        critical_alerts = Alert.objects.filter(severity='CRITICAL', status='ACTIVE').count()
        
        return Response({
            'message': 'Statistiques de la plateforme.',
            'data': {
                'users': {
                    'total': total_users,
                    'patients': total_patients,
                    'caregivers': total_caregivers,
                    'admins': total_admins,
                },
                'pregnancies': {
                    'total': total_pregnancies,
                    'active': active_pregnancies,
                },
                'appointments': {
                    'total': total_appointments,
                    'pending': pending_appointments,
                    'completed': completed_appointments,
                },
                'consultations': {
                    'total': total_consultations,
                },
                'exams': {
                    'total': total_exams,
                },
                'alerts': {
                    'total': total_alerts,
                    'active': active_alerts,
                    'critical': critical_alerts,
                }
            }
        }, status=status.HTTP_200_OK)


# ============================================================
# 3. SUPERVISION DES ALERTES
# ============================================================

class AdminAlertListView(APIView):
    """
    GET /api/v1/admin/alerts - Supervision des alertes
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @extend_schema(
        summary="Supervision des alertes",
        description="Récupère toutes les alertes de la plateforme pour supervision.",
        responses={200: AlertSerializer(many=True)},
        tags=["Administrateur"]
    )
    def get(self, request):
        alerts = Alert.objects.all().order_by('-created_at')
        
        # Filtrer par statut si demandé
        status_filter = request.query_params.get('status')
        if status_filter:
            alerts = alerts.filter(status=status_filter)
        
        # Filtrer par sévérité si demandé
        severity_filter = request.query_params.get('severity')
        if severity_filter:
            alerts = alerts.filter(severity=severity_filter)
        
        return Response({
            'message': 'Liste des alertes.',
            'data': AlertSerializer(alerts, many=True).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 4. CONSULTATION DES LOGS
# ============================================================

class AdminLogListView(APIView):
    """
    GET /api/v1/admin/logs - Journalisation des actions sensibles
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @extend_schema(
        summary="Journalisation des actions",
        description="Consulte les logs des actions sensibles de la plateforme.",
        responses={
            200: OpenApiResponse(
                description="Logs récupérés",
                response={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "user": {"type": "object"},
                                    "action": {"type": "string"},
                                    "description": {"type": "string"},
                                    "ip_address": {"type": "string"},
                                    "created_at": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            )
        },
        tags=["Administrateur"]
    )
    def get(self, request):
        # Récupérer les logs des 7 derniers jours par défaut
        days = int(request.query_params.get('days', 7))
        since = datetime.now() - timedelta(days=days)
        
        logs = AuditLog.objects.filter(
            created_at__gte=since
        ).order_by('-created_at')
        
        # Limiter à 100 logs pour performance
        logs = logs[:100]
        
        return Response({
            'message': f'Logs des {days} derniers jours.',
            'data': [
                {
                    'id': log.id,
                    'user': {
                        'id': log.user.id,
                        'username': log.user.username,
                        'email': log.user.email,
                    },
                    'action': log.action,
                    'description': log.description,
                    'ip_address': log.ip_address,
                    'created_at': log.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                for log in logs
            ]
        }, status=status.HTTP_200_OK)


# ============================================================
# 5. GESTION DES TYPES D'EXAMENS (à implémenter)
# ============================================================

# Note : Cette fonctionnalité peut être ajoutée si vous avez un modèle ExamType
# Pour l'instant, nous utilisons les choix prédéfinis dans MedicalExam

class AdminExamTypeView(APIView):
    """
    GET /api/v1/admin/exam-types - Liste des types d'examens disponibles
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @extend_schema(
        summary="Types d'examens disponibles",
        description="Récupère la liste des types d'examens prédéfinis.",
        responses={
            200: OpenApiResponse(
                description="Types d'examens",
                response={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "data": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "string"},
                                    "label": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            )
        },
        tags=["Administrateur"]
    )
    def get(self, request):
        exam_types = [
            {'value': 'BLOOD', 'label': 'Prise de sang'},
            {'value': 'URINE', 'label': "Analyse d'urine"},
            {'value': 'ULTRASOUND', 'label': 'Échographie'},
            {'value': 'BLOOD_PRESSURE', 'label': 'Tension artérielle'},
            {'value': 'WEIGHT', 'label': 'Poids'},
            {'value': 'OTHER', 'label': 'Autre'},
        ]
        
        return Response({
            'message': 'Types d\'examens disponibles.',
            'data': exam_types
        }, status=status.HTTP_200_OK)