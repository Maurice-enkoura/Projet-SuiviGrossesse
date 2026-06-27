"""
Sérialiseurs pour l'API SuiviGrossesse
"""

from rest_framework import serializers
from .models import (
    User, Pregnancy, Appointment, Consultation, 
    MedicalExam, VitalSign, Alert, FollowUpSchedule,
    Message, DoctorSchedule, Symptom, MedicalHistory,
    Reminder, GrowthMeasurement
)


# ============================================================
# SÉRIALISEURS POUR L'AUTHENTIFICATION
# ============================================================

class UserPublicSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_display', 
                  'speciality', 'phone', 'date_of_birth', 'is_active', 
                  'created_at']
        read_only_fields = ['id', 'created_at', 'is_active']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='PATIENTE', required=False)
    speciality = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                'password_confirmation': 'Les mots de passe ne correspondent pas.'
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# ============================================================
# SÉRIALISEURS POUR LES GROSSESSES
# ============================================================

class PregnancySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.username', read_only=True)
    patient_id = serializers.IntegerField(source='patient.id', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    loss_type_display = serializers.CharField(source='get_loss_type_display', read_only=True)
    
    class Meta:
        model = Pregnancy
        fields = [
            'id', 'patient', 'patient_name', 'patient_id',
            'start_date', 'expected_delivery_date', 'actual_delivery_date',
            'status', 'status_display', 'is_active',
            'loss_date', 'loss_reason', 'loss_type', 'loss_type_display',
            'current_week', 'weight_gain', 'blood_type', 'risk_factors',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'current_week']


class PregnancyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregnancy
        fields = ['start_date', 'expected_delivery_date', 'notes']


class PregnancyLossSerializer(serializers.Serializer):
    loss_type = serializers.ChoiceField(choices=Pregnancy.LOSS_TYPE_CHOICES)
    loss_date = serializers.DateField()
    loss_reason = serializers.CharField(required=False, allow_blank=True)


# ============================================================
# SÉRIALISEURS POUR LES RENDEZ-VOUS
# ============================================================

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.username', read_only=True)
    caregiver_name = serializers.CharField(source='caregiver.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'caregiver', 'caregiver_name',
            'pregnancy', 'date_time', 'duration_minutes', 'reason',
            'status', 'status_display', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['caregiver', 'pregnancy', 'date_time', 'duration_minutes', 'reason']


# ============================================================
# SÉRIALISEURS POUR LES CONSULTATIONS
# ============================================================

class ConsultationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='appointment.patient.username', read_only=True)
    caregiver_name = serializers.CharField(source='appointment.caregiver.username', read_only=True)
    
    class Meta:
        model = Consultation
        fields = [
            'id', 'appointment', 'patient_name', 'caregiver_name',
            'consultation_date', 'report', 'blood_pressure',
            'weight', 'urine_test', 'fetal_heartbeat', 'observations',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'consultation_date', 'created_at', 'updated_at']


# ============================================================
# SÉRIALISEURS POUR LES EXAMENS MÉDICAUX
# ============================================================

class MedicalExamSerializer(serializers.ModelSerializer):
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)
    
    class Meta:
        model = MedicalExam
        fields = [
            'id', 'consultation', 'exam_type', 'exam_type_display',
            'exam_date', 'result_summary', 'details',
            'is_abnormal', 'file_attachment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'exam_date', 'created_at', 'updated_at']


# ============================================================
# SÉRIALISEURS POUR LES CONSTANTES MÉDICALES
# ============================================================

class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = [
            'id', 'consultation', 'weight_kg', 'blood_pressure_systolic',
            'blood_pressure_diastolic', 'uterine_height', 'fetal_heart_rate',
            'fetal_movements', 'observations', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================
# SÉRIALISEURS POUR LES ALERTES
# ============================================================

class AlertSerializer(serializers.ModelSerializer):
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Alert
        fields = [
            'id', 'consultation', 'alert_type', 'alert_type_display',
            'severity', 'severity_display', 'status', 'status_display',
            'description', 'action_taken', 'acknowledged_at', 'resolved_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================
# SÉRIALISEURS POUR LE CALENDRIER DE SUIVI
# ============================================================

class FollowUpScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpSchedule
        fields = [
            'id', 'pregnancy', 'title', 'description',
            'scheduled_date', 'is_completed', 'completed_date',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================
# SÉRIALISEURS POUR LA MESSAGERIE
# ============================================================

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    sender_role = serializers.CharField(source='sender.role', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_name', 'sender_role',
            'recipient', 'recipient_name',
            'pregnancy', 'subject', 'content',
            'is_read', 'read_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================
# SÉRIALISEURS POUR LES HORAIRES
# ============================================================

class DoctorScheduleSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = DoctorSchedule
        fields = [
            'id', 'doctor', 'day_of_week', 'day_display',
            'is_working', 'morning_start', 'morning_end',
            'afternoon_start', 'afternoon_end', 'slot_duration',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================
# ⭐ NOUVEAUX SÉRIALISEURS
# ============================================================

class SymptomSerializer(serializers.ModelSerializer):
    symptom_type_display = serializers.CharField(source='get_symptom_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = Symptom
        fields = [
            'id', 'patient', 'pregnancy', 'symptom_type', 'symptom_type_display',
            'severity', 'severity_display', 'date', 'notes',
            'resolved', 'resolved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date', 'created_at', 'updated_at']


class MedicalHistorySerializer(serializers.ModelSerializer):
    condition_type_display = serializers.CharField(source='get_condition_type_display', read_only=True)
    
    class Meta:
        model = MedicalHistory
        fields = [
            'id', 'patient', 'condition_type', 'condition_type_display',
            'condition_name', 'diagnosed_at', 'notes',
            'resolved', 'resolved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReminderSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Reminder
        fields = [
            'id', 'patient', 'pregnancy', 'title', 'description',
            'reminder_date', 'type', 'type_display',
            'is_sent', 'sent_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GrowthMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthMeasurement
        fields = [
            'id', 'pregnancy', 'date', 'week',
            'weight_estimated', 'height_estimated',
            'fetal_heart_rate', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date', 'created_at', 'updated_at']