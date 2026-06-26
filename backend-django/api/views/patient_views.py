"""
Vues pour les PATIENTES
Gestion des grossesses, rendez-vous, examens, constantes, suivi, alertes
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..models import (
    User, Pregnancy, Appointment, Consultation, 
    MedicalExam, VitalSign, Alert, FollowUpSchedule, AuditLog
)
from ..serializers import (
    PregnancySerializer, PregnancyCreateSerializer,
    AppointmentSerializer, AppointmentCreateSerializer,
    MedicalExamSerializer, VitalSignSerializer,
    AlertSerializer, FollowUpScheduleSerializer
)
from ..permissions import IsPatient


# ============================================================
# 1. GESTION DES GROSSESSES
# ============================================================

class PatientPregnancyListView(APIView):
    """
    GET /api/v1/patient/pregnancies - Liste des grossesses de la patiente
    POST /api/v1/patient/pregnancies - Créer une nouvelle grossesse
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    @extend_schema(
        summary="Liste des grossesses",
        description="Récupère toutes les grossesses de la patiente connectée.",
        responses={200: PregnancySerializer(many=True)},
        tags=["Patiente - Grossesse"]
    )
    def get(self, request):
        pregnancies = Pregnancy.objects.filter(patient=request.user).order_by('-created_at')
        return Response({
            'message': 'Liste des grossesses.',
            'data': PregnancySerializer(pregnancies, many=True).data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Créer une grossesse",
        description="Crée une nouvelle grossesse pour la patiente connectée.",
        request=PregnancyCreateSerializer,
        responses={201: PregnancySerializer},
        tags=["Patiente - Grossesse"]
    )
    def post(self, request):
        # Vérifier si la patiente a déjà une grossesse active
        if Pregnancy.objects.filter(patient=request.user, is_active=True).exists():
            return Response({
                'message': 'Vous avez déjà une grossesse active.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PregnancyCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        pregnancy = Pregnancy.objects.create(
            patient=request.user,
            **serializer.validated_data,
            is_active=True
        )
        
        # Journaliser l'action
        AuditLog.objects.create(
            user=request.user,
            action='CREATE_PREGNANCY',
            description=f"Création d'une grossesse pour {request.user.email}",
        )
        
        return Response({
            'message': 'Grossesse créée avec succès.',
            'data': PregnancySerializer(pregnancy).data
        }, status=status.HTTP_201_CREATED)


class PatientPregnancyDetailView(APIView):
    """
    GET /api/v1/patient/pregnancies/<id> - Détail d'une grossesse
    PUT /api/v1/patient/pregnancies/<id> - Modifier une grossesse
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get_pregnancy(self, pk, user):
        try:
            return Pregnancy.objects.get(pk=pk, patient=user)
        except Pregnancy.DoesNotExist:
            return None
    
    @extend_schema(
        summary="Détail d'une grossesse",
        description="Récupère les détails d'une grossesse spécifique.",
        responses={200: PregnancySerializer, 404: OpenApiResponse(description="Grossesse non trouvée")},
        tags=["Patiente - Grossesse"]
    )
    def get(self, request, pk):
        pregnancy = self.get_pregnancy(pk, request.user)
        if not pregnancy:
            return Response({
                'message': 'Grossesse non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'message': 'Détail de la grossesse.',
            'data': PregnancySerializer(pregnancy).data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Modifier une grossesse",
        description="Modifie les informations d'une grossesse.",
        request=PregnancyCreateSerializer,
        responses={200: PregnancySerializer, 404: OpenApiResponse(description="Grossesse non trouvée")},
        tags=["Patiente - Grossesse"]
    )
    def put(self, request, pk):
        pregnancy = self.get_pregnancy(pk, request.user)
        if not pregnancy:
            return Response({
                'message': 'Grossesse non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PregnancyCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        for key, value in serializer.validated_data.items():
            setattr(pregnancy, key, value)
        pregnancy.save()
        
        return Response({
            'message': 'Grossesse mise à jour.',
            'data': PregnancySerializer(pregnancy).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 2. GESTION DES RENDEZ-VOUS
# ============================================================

class PatientAppointmentListView(APIView):
    """
    GET /api/v1/patient/appointments - Liste des rendez-vous
    POST /api/v1/patient/appointments - Créer un rendez-vous
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    @extend_schema(
        summary="Liste des rendez-vous",
        description="Récupère tous les rendez-vous de la patiente connectée.",
        responses={200: AppointmentSerializer(many=True)},
        tags=["Patiente - Rendez-vous"]
    )
    def get(self, request):
        appointments = Appointment.objects.filter(
            patient=request.user
        ).order_by('-date_time')
        return Response({
            'message': 'Liste des rendez-vous.',
            'data': AppointmentSerializer(appointments, many=True).data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Créer un rendez-vous",
        description="Crée un nouveau rendez-vous pour la patiente.",
        request=AppointmentCreateSerializer,
        responses={201: AppointmentSerializer},
        tags=["Patiente - Rendez-vous"]
    )
    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        data = serializer.validated_data
        
        # Vérifier que la grossesse appartient à la patiente
        pregnancy = data['pregnancy']
        if pregnancy.patient != request.user:
            return Response({
                'message': 'Cette grossesse ne vous appartient pas.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        appointment = Appointment.objects.create(
            patient=request.user,
            **data,
            status='SCHEDULED'
        )
        
        return Response({
            'message': 'Rendez-vous créé avec succès.',
            'data': AppointmentSerializer(appointment).data
        }, status=status.HTTP_201_CREATED)


class PatientAppointmentCancelView(APIView):
    """
    POST /api/v1/patient/appointments/<id>/cancel - Annuler un rendez-vous
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    @extend_schema(
        summary="Annuler un rendez-vous",
        description="Annule un rendez-vous non encore effectué.",
        responses={200: OpenApiResponse(description="Rendez-vous annulé"), 404: OpenApiResponse(description="Rendez-vous non trouvé")},
        tags=["Patiente - Rendez-vous"]
    )
    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, patient=request.user)
        except Appointment.DoesNotExist:
            return Response({
                'message': 'Rendez-vous non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier si le rendez-vous peut être annulé
        if appointment.status == 'CANCELLED':
            return Response({
                'message': 'Ce rendez-vous est déjà annulé.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if appointment.status == 'COMPLETED':
            return Response({
                'message': 'Impossible d\'annuler un rendez-vous déjà effectué.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        appointment.status = 'CANCELLED'
        appointment.save()
        
        return Response({
            'message': 'Rendez-vous annulé avec succès.',
            'data': AppointmentSerializer(appointment).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 3. CONSULTATION DES EXAMENS
# ============================================================

class PatientExamListView(APIView):
    """
    GET /api/v1/patient/exams - Liste des examens de la patiente
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    @extend_schema(
        summary="Liste des examens",
        description="Récupère tous les examens de la patiente connectée.",
        responses={200: MedicalExamSerializer(many=True)},
        tags=["Patiente - Examens"]
    )
    def get(self, request):
        exams = MedicalExam.objects.filter(
            consultation__appointment__patient=request.user
        ).order_by('-exam_date')
        return Response({
            'message': 'Liste des examens.',
            'data': MedicalExamSerializer(exams, many=True).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 4. CONSULTATION DES CONSTANTES MÉDICALES
# ============================================================

class PatientVitalSignListView(APIView):
    """
    GET /api/v1/patient/vital-signs - Liste des constantes médicales
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    @extend_schema(
        summary="Liste des constantes médicales",
        description="Récupère toutes les constantes de la patiente connectée.",
        responses={200: VitalSignSerializer(many=True)},
        tags=["Patiente - Suivi"]
    )
    def get(self, request):
        vital_signs = VitalSign.objects.filter(
            consultation__appointment__patient=request.user
        ).order_by('-created_at')
        return Response({
            'message': 'Liste des constantes médicales.',
            'data': VitalSignSerializer(vital_signs, many=True).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 5. CONSULTATION DU CALENDRIER DE SUIVI
# ============================================================

class PatientFollowUpView(APIView):
    """
    GET /api/v1/patient/follow-up - Calendrier de suivi
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    @extend_schema(
        summary="Calendrier de suivi",
        description="Récupère le calendrier de suivi de la grossesse active.",
        responses={200: FollowUpScheduleSerializer(many=True)},
        tags=["Patiente - Suivi"]
    )
    def get(self, request):
        try:
            pregnancy = Pregnancy.objects.get(patient=request.user, is_active=True)
        except Pregnancy.DoesNotExist:
            return Response({
                'message': 'Aucune grossesse active trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        schedule = FollowUpSchedule.objects.filter(
            pregnancy=pregnancy
        ).order_by('scheduled_date')
        
        return Response({
            'message': 'Calendrier de suivi.',
            'data': FollowUpScheduleSerializer(schedule, many=True).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 6. CONSULTATION DES ALERTES
# ============================================================

class PatientAlertListView(APIView):
    """
    GET /api/v1/patient/alerts - Liste des alertes de la patiente
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    @extend_schema(
        summary="Liste des alertes",
        description="Récupère toutes les alertes concernant la patiente connectée.",
        responses={200: AlertSerializer(many=True)},
        tags=["Patiente - Suivi"]
    )
    def get(self, request):
        alerts = Alert.objects.filter(
            consultation__appointment__patient=request.user
        ).order_by('-created_at')
        return Response({
            'message': 'Liste des alertes.',
            'data': AlertSerializer(alerts, many=True).data
        }, status=status.HTTP_200_OK)