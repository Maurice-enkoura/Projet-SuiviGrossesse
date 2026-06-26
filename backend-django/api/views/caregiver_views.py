"""
Vues pour les SOIGNANTS
Gestion des patientes, consultations, examens, constantes, alertes
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from datetime import datetime

from ..models import (
    User, Pregnancy, Appointment, Consultation, 
    MedicalExam, VitalSign, Alert, FollowUpSchedule, AuditLog, UserCaregiver
)
from ..serializers import (
    UserPublicSerializer,
    PregnancySerializer,
    AppointmentSerializer, AppointmentCreateSerializer,
    ConsultationSerializer,
    MedicalExamSerializer,
    VitalSignSerializer,
    AlertSerializer
)
from ..permissions import IsCaregiver


# ============================================================
# 1. GESTION DES PATIENTES
# ============================================================

class CaregiverPatientListView(APIView):
    """
    GET /api/v1/caregiver/patients - Liste des patientes attribuées au soignant
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Liste des patientes",
        description="Récupère toutes les patientes attribuées au soignant connecté.",
        responses={200: UserPublicSerializer(many=True)},
        tags=["Soignant - Patient"]
    )
    def get(self, request):
        # Récupérer les patientes attribuées via la table de liaison
        patient_assignments = UserCaregiver.objects.filter(caregiver=request.user)
        patients = [assignment.patient for assignment in patient_assignments]
        
        return Response({
            'message': 'Liste des patientes attribuées.',
            'data': UserPublicSerializer(patients, many=True).data
        }, status=status.HTTP_200_OK)


class CaregiverPatientDetailView(APIView):
    """
    GET /api/v1/caregiver/patients/<id> - Dossier complet d'une patiente
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Dossier d'une patiente",
        description="Récupère le dossier complet d'une patiente attribuée.",
        responses={
            200: OpenApiResponse(description="Dossier récupéré"),
            403: OpenApiResponse(description="Accès interdit"),
            404: OpenApiResponse(description="Patiente non trouvée")
        },
        tags=["Soignant - Patient"]
    )
    def get(self, request, pk):
        # Vérifier que la patiente est attribuée au soignant
        try:
            assignment = UserCaregiver.objects.get(patient_id=pk, caregiver=request.user)
        except UserCaregiver.DoesNotExist:
            return Response({
                'message': 'Cette patiente ne vous est pas attribuée.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            patient = User.objects.get(pk=pk, role='PATIENTE')
        except User.DoesNotExist:
            return Response({
                'message': 'Patiente non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Récupérer toutes les données de la patiente
        pregnancies = Pregnancy.objects.filter(patient=patient)
        appointments = Appointment.objects.filter(patient=patient)
        consultations = Consultation.objects.filter(appointment__patient=patient)
        exams = MedicalExam.objects.filter(consultation__appointment__patient=patient)
        vital_signs = VitalSign.objects.filter(consultation__appointment__patient=patient)
        alerts = Alert.objects.filter(consultation__appointment__patient=patient)
        
        return Response({
            'message': 'Dossier de la patiente.',
            'patient': UserPublicSerializer(patient).data,
            'pregnancies': PregnancySerializer(pregnancies, many=True).data,
            'appointments': AppointmentSerializer(appointments, many=True).data,
            'consultations': ConsultationSerializer(consultations, many=True).data,
            'exams': MedicalExamSerializer(exams, many=True).data,
            'vital_signs': VitalSignSerializer(vital_signs, many=True).data,
            'alerts': AlertSerializer(alerts, many=True).data,
        }, status=status.HTTP_200_OK)


# ============================================================
# 2. GESTION DES RENDEZ-VOUS
# ============================================================

class CaregiverAppointmentListView(APIView):
    """
    GET /api/v1/caregiver/appointments - Rendez-vous du soignant
    POST /api/v1/caregiver/appointments - Planifier un rendez-vous
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Liste des rendez-vous",
        description="Récupère tous les rendez-vous du soignant connecté.",
        responses={200: AppointmentSerializer(many=True)},
        tags=["Soignant - Rendez-vous"]
    )
    def get(self, request):
        appointments = Appointment.objects.filter(
            caregiver=request.user
        ).order_by('date_time')
        
        return Response({
            'message': 'Liste des rendez-vous.',
            'data': AppointmentSerializer(appointments, many=True).data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Planifier un rendez-vous",
        description="Crée un rendez-vous pour une patiente attribuée.",
        request=AppointmentCreateSerializer,
        responses={201: AppointmentSerializer},
        tags=["Soignant - Rendez-vous"]
    )
    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        data = serializer.validated_data
        
        # Vérifier que la patiente est attribuée au soignant
        try:
            UserCaregiver.objects.get(patient=data['pregnancy'].patient, caregiver=request.user)
        except UserCaregiver.DoesNotExist:
            return Response({
                'message': 'Cette patiente ne vous est pas attribuée.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Créer le rendez-vous
        appointment = Appointment.objects.create(
            patient=data['pregnancy'].patient,
            caregiver=request.user,
            **data,
            status='SCHEDULED'
        )
        
        # Journaliser l'action
        AuditLog.objects.create(
            user=request.user,
            action='CREATE_APPOINTMENT',
            description=f"Planification d'un rendez-vous pour {appointment.patient.email}",
        )
        
        return Response({
            'message': 'Rendez-vous planifié avec succès.',
            'data': AppointmentSerializer(appointment).data
        }, status=status.HTTP_201_CREATED)


class CaregiverAppointmentStatusView(APIView):
    """
    POST /api/v1/caregiver/appointments/<id>/status - Changer le statut d'un rendez-vous
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Changer le statut d'un rendez-vous",
        description="Permet de passer un rendez-vous de SCHEDULED à CONFIRMED ou COMPLETED.",
        request={
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["CONFIRMED", "COMPLETED"],
                    "description": "Nouveau statut du rendez-vous"
                }
            }
        },
        responses={200: AppointmentSerializer},
        tags=["Soignant - Rendez-vous"]
    )
    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, caregiver=request.user)
        except Appointment.DoesNotExist:
            return Response({
                'message': 'Rendez-vous non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier le statut actuel
        if appointment.status == 'CANCELLED':
            return Response({
                'message': 'Ce rendez-vous est annulé.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if appointment.status == 'COMPLETED':
            return Response({
                'message': 'Ce rendez-vous est déjà effectué.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupérer le nouveau statut
        new_status = request.data.get('status')
        if new_status not in ['CONFIRMED', 'COMPLETED']:
            return Response({
                'message': 'Statut invalide. Utilisez CONFIRMED ou COMPLETED.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        appointment.status = new_status
        appointment.save()
        
        # Si le rendez-vous est COMPLETED, créer automatiquement une consultation
        if new_status == 'COMPLETED':
            consultation = Consultation.objects.create(
                appointment=appointment,
                report="Consultation réalisée. Compte-rendu à compléter."
            )
        
        return Response({
            'message': f'Statut du rendez-vous mis à jour : {new_status}',
            'data': AppointmentSerializer(appointment).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 3. GESTION DES CONSULTATIONS
# ============================================================

class CaregiverConsultationCreateView(APIView):
    """
    POST /api/v1/caregiver/consultations - Ajouter une consultation
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Ajouter une consultation",
        description="Crée une consultation à partir d'un rendez-vous effectué.",
        request={
            "type": "object",
            "properties": {
                "appointment_id": {"type": "integer"},
                "report": {"type": "string", "description": "Compte-rendu médical"}
            },
            "required": ["appointment_id", "report"]
        },
        responses={201: ConsultationSerializer},
        tags=["Soignant - Consultation"]
    )
    def post(self, request):
        appointment_id = request.data.get('appointment_id')
        report = request.data.get('report')
        
        if not appointment_id or not report:
            return Response({
                'message': 'appointment_id et report sont requis.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            appointment = Appointment.objects.get(pk=appointment_id, caregiver=request.user)
        except Appointment.DoesNotExist:
            return Response({
                'message': 'Rendez-vous non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if appointment.status != 'COMPLETED':
            return Response({
                'message': 'Impossible d\'ajouter une consultation pour un rendez-vous non effectué.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier qu'une consultation n'existe pas déjà
        if Consultation.objects.filter(appointment=appointment).exists():
            return Response({
                'message': 'Une consultation existe déjà pour ce rendez-vous.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        consultation = Consultation.objects.create(
            appointment=appointment,
            report=report
        )
        
        return Response({
            'message': 'Consultation ajoutée avec succès.',
            'data': ConsultationSerializer(consultation).data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# 4. GESTION DES EXAMENS MÉDICAUX
# ============================================================

class CaregiverExamCreateView(APIView):
    """
    POST /api/v1/caregiver/exams - Ajouter un examen médical
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Ajouter un examen médical",
        description="Ajoute un examen médical à une consultation existante.",
        request=MedicalExamSerializer,
        responses={201: MedicalExamSerializer},
        tags=["Soignant - Consultation"]
    )
    def post(self, request):
        consultation_id = request.data.get('consultation')
        
        try:
            consultation = Consultation.objects.get(pk=consultation_id)
        except Consultation.DoesNotExist:
            return Response({
                'message': 'Consultation non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier que le soignant a accès à cette consultation
        if consultation.appointment.caregiver != request.user:
            return Response({
                'message': 'Vous n\'avez pas accès à cette consultation.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = MedicalExamSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        exam = MedicalExam.objects.create(
            consultation=consultation,
            **serializer.validated_data
        )
        
        return Response({
            'message': 'Examen ajouté avec succès.',
            'data': MedicalExamSerializer(exam).data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# 5. ENREGISTREMENT DES CONSTANTES MÉDICALES
# ============================================================

class CaregiverVitalSignCreateView(APIView):
    """
    POST /api/v1/caregiver/vital-signs - Enregistrer des constantes médicales
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Enregistrer des constantes médicales",
        description="Enregistre les constantes d'une patiente lors d'une consultation.",
        request=VitalSignSerializer,
        responses={201: VitalSignSerializer},
        tags=["Soignant - Consultation"]
    )
    def post(self, request):
        consultation_id = request.data.get('consultation')
        
        try:
            consultation = Consultation.objects.get(pk=consultation_id)
        except Consultation.DoesNotExist:
            return Response({
                'message': 'Consultation non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if consultation.appointment.caregiver != request.user:
            return Response({
                'message': 'Vous n\'avez pas accès à cette consultation.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Vérifier que des constantes n'existent pas déjà
        if VitalSign.objects.filter(consultation=consultation).exists():
            return Response({
                'message': 'Des constantes ont déjà été enregistrées pour cette consultation.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = VitalSignSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        vital_sign = VitalSign.objects.create(
            consultation=consultation,
            **serializer.validated_data
        )
        
        # Vérifier les seuils d'alerte
        self.check_alert_thresholds(vital_sign, consultation)
        
        return Response({
            'message': 'Constantes enregistrées avec succès.',
            'data': VitalSignSerializer(vital_sign).data
        }, status=status.HTTP_201_CREATED)
    
    def check_alert_thresholds(self, vital_sign, consultation):
        """Vérifie les seuils d'alerte et crée une alerte si nécessaire"""
        alerts = []
        
        # Vérifier la tension artérielle
        if vital_sign.blood_pressure_systolic and vital_sign.blood_pressure_diastolic:
            if vital_sign.blood_pressure_systolic > 140 or vital_sign.blood_pressure_diastolic > 90:
                alerts.append({
                    'type': 'HYPERTENSION',
                    'severity': 'HIGH',
                    'description': f"Hypertension détectée : {vital_sign.blood_pressure_systolic}/{vital_sign.blood_pressure_diastolic} mmHg"
                })
        
        # Créer les alertes si nécessaires
        for alert_data in alerts:
            Alert.objects.create(
                consultation=consultation,
                alert_type=alert_data['type'],
                severity=alert_data['severity'],
                description=alert_data['description']
            )


# ============================================================
# 6. DÉCLARATION DES ALERTES MÉDICALES
# ============================================================

class CaregiverAlertCreateView(APIView):
    """
    POST /api/v1/caregiver/alerts - Déclarer une alerte médicale
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Déclarer une alerte médicale",
        description="""
        Déclare une alerte médicale ou urgence obstétricale.
        
        Types d'alertes :
        - HYPERTENSION : Hypertension
        - BLEEDING : Saignement
        - PRETERM_RISK : Risque d'accouchement prématuré
        - GESTATIONAL_DIABETES : Diabète gestationnel
        - OTHER : Autre complication
        
        Niveaux de sévérité :
        - LOW : Faible
        - MEDIUM : Moyen
        - HIGH : Élevé
        - CRITICAL : Critique
        """,
        request=AlertSerializer,
        responses={201: AlertSerializer},
        tags=["Soignant - Alerte"]
    )
    def post(self, request):
        consultation_id = request.data.get('consultation')
        
        try:
            consultation = Consultation.objects.get(pk=consultation_id)
        except Consultation.DoesNotExist:
            return Response({
                'message': 'Consultation non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if consultation.appointment.caregiver != request.user:
            return Response({
                'message': 'Vous n\'avez pas accès à cette consultation.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AlertSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        alert = Alert.objects.create(
            consultation=consultation,
            **serializer.validated_data
        )
        
        # Journaliser l'action
        AuditLog.objects.create(
            user=request.user,
            action='CREATE_ALERT',
            description=f"Alerte déclarée : {alert.get_alert_type_display()} - {alert.get_severity_display()}",
        )
        
        return Response({
            'message': 'Alerte déclarée avec succès.',
            'data': AlertSerializer(alert).data
        }, status=status.HTTP_201_CREATED)


class CaregiverAlertListView(APIView):
    """
    GET /api/v1/caregiver/alerts - Liste des alertes du soignant
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    @extend_schema(
        summary="Liste des alertes",
        description="Récupère toutes les alertes déclarées par le soignant.",
        responses={200: AlertSerializer(many=True)},
        tags=["Soignant - Alerte"]
    )
    def get(self, request):
        alerts = Alert.objects.filter(
            consultation__appointment__caregiver=request.user
        ).order_by('-created_at')
        
        return Response({
            'message': 'Liste des alertes.',
            'data': AlertSerializer(alerts, many=True).data
        }, status=status.HTTP_200_OK)


class CaregiverAlertDetailView(APIView):
    """
    GET /api/v1/caregiver/alerts/<id> - Détail d'une alerte
    PUT /api/v1/caregiver/alerts/<id> - Mettre à jour une alerte
    """
    permission_classes = [IsAuthenticated, IsCaregiver]
    
    def get_alert(self, pk, user):
        try:
            return Alert.objects.get(pk=pk, consultation__appointment__caregiver=user)
        except Alert.DoesNotExist:
            return None
    
    @extend_schema(
        summary="Détail d'une alerte",
        description="Récupère les détails d'une alerte spécifique.",
        responses={200: AlertSerializer, 404: OpenApiResponse(description="Alerte non trouvée")},
        tags=["Soignant - Alerte"]
    )
    def get(self, request, pk):
        alert = self.get_alert(pk, request.user)
        if not alert:
            return Response({
                'message': 'Alerte non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'message': 'Détail de l\'alerte.',
            'data': AlertSerializer(alert).data
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Mettre à jour une alerte",
        description="Met à jour le statut ou les actions d'une alerte.",
        request=AlertSerializer,
        responses={200: AlertSerializer},
        tags=["Soignant - Alerte"]
    )
    def put(self, request, pk):
        alert = self.get_alert(pk, request.user)
        if not alert:
            return Response({
                'message': 'Alerte non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AlertSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        for key, value in serializer.validated_data.items():
            setattr(alert, key, value)
        
        # Mettre à jour les dates selon le statut
        if alert.status == 'ACKNOWLEDGED' and not alert.acknowledged_at:
            alert.acknowledged_at = datetime.now()
        elif alert.status == 'RESOLVED' and not alert.resolved_at:
            alert.resolved_at = datetime.now()
        
        alert.save()
        
        return Response({
            'message': 'Alerte mise à jour.',
            'data': AlertSerializer(alert).data
        }, status=status.HTTP_200_OK)


        # backend/api/views/caregiver_views.py - Ajouter la gestion des fichiers

class CaregiverConsultationCreateView(APIView):
    def post(self, request):
        appointment_id = request.data.get('appointment_id')
        report = request.data.get('report')
        files = request.FILES.getlist('files')
        
        if not appointment_id or not report:
            return Response({
                'message': 'appointment_id et report sont requis.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            appointment = Appointment.objects.get(pk=appointment_id, caregiver=request.user)
        except Appointment.DoesNotExist:
            return Response({
                'message': 'Rendez-vous non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if appointment.status != 'COMPLETED':
            return Response({
                'message': 'Impossible d\'ajouter une consultation pour un rendez-vous non effectué.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        consultation = Consultation.objects.create(
            appointment=appointment,
            report=report
        )
        
        # Traiter les fichiers
        for file in files:
            # Créer un examen avec le fichier
            MedicalExam.objects.create(
                consultation=consultation,
                exam_type='OTHER',
                result_summary=f'Fichier: {file.name}',
                file_attachment=file
            )
        
        return Response({
            'message': 'Consultation ajoutée avec succès.',
            'data': ConsultationSerializer(consultation).data
        }, status=status.HTTP_201_CREATED)