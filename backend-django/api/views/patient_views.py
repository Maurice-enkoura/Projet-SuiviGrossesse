"""
Vues pour les PATIENTES
Gestion des grossesses, rendez-vous, examens, constantes, suivi, alertes, symptômes, historique
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from datetime import datetime

from ..models import (
    User, Pregnancy, Appointment, Consultation, 
    MedicalExam, VitalSign, Alert, FollowUpSchedule, 
    AuditLog, Symptom, MedicalHistory, Reminder, GrowthMeasurement
)
from ..serializers import (
    PregnancySerializer, PregnancyCreateSerializer, PregnancyLossSerializer,
    AppointmentSerializer, AppointmentCreateSerializer,
    MedicalExamSerializer, VitalSignSerializer,
    AlertSerializer, FollowUpScheduleSerializer,
    SymptomSerializer, MedicalHistorySerializer,
    ReminderSerializer, GrowthMeasurementSerializer
)
from ..permissions import IsPatient


# ============================================================
# 1. GESTION DES GROSSESSES (avec perte et accouchement)
# ============================================================

class PatientPregnancyListView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request):
        pregnancies = Pregnancy.objects.filter(patient=request.user).order_by('-created_at')
        return Response({
            'message': 'Liste des grossesses.',
            'data': PregnancySerializer(pregnancies, many=True).data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
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
            is_active=True,
            status='ACTIVE'
        )
        
        # Mettre à jour le total des grossesses
        user = request.user
        user.total_pregnancies += 1
        user.save()
        
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
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get_pregnancy(self, pk, user):
        try:
            return Pregnancy.objects.get(pk=pk, patient=user)
        except Pregnancy.DoesNotExist:
            return None
    
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


class PatientPregnancyLossView(APIView):
    """
    POST /api/v1/patient/pregnancies/<id>/loss - Déclarer une perte de grossesse
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    def post(self, request, pk):
        try:
            pregnancy = Pregnancy.objects.get(pk=pk, patient=request.user)
        except Pregnancy.DoesNotExist:
            return Response({
                'message': 'Grossesse non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if pregnancy.status != 'ACTIVE':
            return Response({
                'message': 'Cette grossesse est déjà terminée.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PregnancyLossSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        data = serializer.validated_data
        
        # Mettre à jour la grossesse
        pregnancy.status = 'LOST'
        pregnancy.is_active = False
        pregnancy.loss_type = data['loss_type']
        pregnancy.loss_date = data['loss_date']
        pregnancy.loss_reason = data.get('loss_reason', '')
        pregnancy.save()
        
        # Mettre à jour les statistiques patiente
        user = request.user
        user.total_miscarriages += 1
        user.is_pregnant = False
        user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='PREGNANCY_LOSS',
            description=f"Perte de grossesse #{pregnancy.id} - {data['loss_type']}",
        )
        
        return Response({
            'message': 'Perte de grossesse déclarée.',
            'data': PregnancySerializer(pregnancy).data
        }, status=status.HTTP_200_OK)


class PatientPregnancyCompleteView(APIView):
    """
    POST /api/v1/patient/pregnancies/<id>/complete - Déclarer un accouchement
    """
    permission_classes = [IsAuthenticated, IsPatient]
    
    def post(self, request, pk):
        try:
            pregnancy = Pregnancy.objects.get(pk=pk, patient=request.user)
        except Pregnancy.DoesNotExist:
            return Response({
                'message': 'Grossesse non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if pregnancy.status != 'ACTIVE':
            return Response({
                'message': 'Cette grossesse est déjà terminée.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        actual_delivery_date = request.data.get('actual_delivery_date')
        if not actual_delivery_date:
            return Response({
                'message': 'La date d\'accouchement est requise.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        pregnancy.status = 'COMPLETED'
        pregnancy.is_active = False
        pregnancy.actual_delivery_date = actual_delivery_date
        pregnancy.save()
        
        # Mettre à jour les statistiques patiente
        user = request.user
        user.total_births += 1
        user.is_pregnant = False
        user.save()
        
        AuditLog.objects.create(
            user=request.user,
            action='PREGNANCY_COMPLETED',
            description=f"Accouchement - Grossesse #{pregnancy.id}",
        )
        
        return Response({
            'message': 'Accouchement déclaré avec succès.',
            'data': PregnancySerializer(pregnancy).data
        }, status=status.HTTP_200_OK)


# ============================================================
# 2. GESTION DES RENDEZ-VOUS
# ============================================================

class PatientAppointmentListView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request):
        appointments = Appointment.objects.filter(
            patient=request.user
        ).order_by('-date_time')
        return Response({
            'message': 'Liste des rendez-vous.',
            'data': AppointmentSerializer(appointments, many=True).data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AppointmentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        data = serializer.validated_data
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
    permission_classes = [IsAuthenticated, IsPatient]
    
    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, patient=request.user)
        except Appointment.DoesNotExist:
            return Response({
                'message': 'Rendez-vous non trouvé.'
            }, status=status.HTTP_404_NOT_FOUND)
        
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
# 3. SYMPTÔMES
# ============================================================

class PatientSymptomListView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request):
        symptoms = Symptom.objects.filter(patient=request.user).order_by('-date')
        return Response({
            'message': 'Liste des symptômes.',
            'data': SymptomSerializer(symptoms, many=True).data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        data['patient'] = request.user.id
        
        serializer = SymptomSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        
        return Response({
            'message': 'Symptôme ajouté avec succès.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# 4. HISTORIQUE MÉDICAL
# ============================================================

class PatientMedicalHistoryView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request):
        history = MedicalHistory.objects.filter(patient=request.user).order_by('-created_at')
        return Response({
            'message': 'Historique médical.',
            'data': MedicalHistorySerializer(history, many=True).data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        data['patient'] = request.user.id
        
        serializer = MedicalHistorySerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        
        return Response({
            'message': 'Antécédent ajouté avec succès.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# 5. RAPPELS
# ============================================================

class PatientReminderListView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request):
        reminders = Reminder.objects.filter(patient=request.user).order_by('reminder_date')
        return Response({
            'message': 'Liste des rappels.',
            'data': ReminderSerializer(reminders, many=True).data
        }, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        data['patient'] = request.user.id
        
        serializer = ReminderSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        
        return Response({
            'message': 'Rappel créé avec succès.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# 6. MESURES DE CROISSANCE
# ============================================================

class PatientGrowthMeasurementView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request, pregnancy_id):
        try:
            pregnancy = Pregnancy.objects.get(pk=pregnancy_id, patient=request.user)
        except Pregnancy.DoesNotExist:
            return Response({
                'message': 'Grossesse non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        measurements = GrowthMeasurement.objects.filter(pregnancy=pregnancy).order_by('week')
        return Response({
            'message': 'Mesures de croissance.',
            'data': GrowthMeasurementSerializer(measurements, many=True).data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, pregnancy_id):
        try:
            pregnancy = Pregnancy.objects.get(pk=pregnancy_id, patient=request.user)
        except Pregnancy.DoesNotExist:
            return Response({
                'message': 'Grossesse non trouvée.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        data['pregnancy'] = pregnancy.id
        
        serializer = GrowthMeasurementSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Erreur de validation.',
                'errors': serializer.errors
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        
        return Response({
            'message': 'Mesure ajoutée avec succès.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# 7. EXAMENS ET CONSTANTES (inchangés)
# ============================================================

class PatientExamListView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request):
        exams = MedicalExam.objects.filter(
            consultation__appointment__patient=request.user
        ).order_by('-exam_date')
        return Response({
            'message': 'Liste des examens.',
            'data': MedicalExamSerializer(exams, many=True).data
        }, status=status.HTTP_200_OK)


class PatientVitalSignListView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request):
        vital_signs = VitalSign.objects.filter(
            consultation__appointment__patient=request.user
        ).order_by('-created_at')
        return Response({
            'message': 'Liste des constantes médicales.',
            'data': VitalSignSerializer(vital_signs, many=True).data
        }, status=status.HTTP_200_OK)


class PatientFollowUpView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
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


class PatientAlertListView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def get(self, request):
        alerts = Alert.objects.filter(
            consultation__appointment__patient=request.user
        ).order_by('-created_at')
        return Response({
            'message': 'Liste des alertes.',
            'data': AlertSerializer(alerts, many=True).data
        }, status=status.HTTP_200_OK)