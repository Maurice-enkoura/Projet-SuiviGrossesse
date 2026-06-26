"""
Sérialiseurs pour l'API SuiviGrossesse
"""

from rest_framework import serializers
from .models import (
    User, Pregnancy, Appointment, Consultation, 
    MedicalExam, VitalSign, Alert, FollowUpSchedule,
    Message, DoctorSchedule
)


# ============================================================
# SÉRIALISEURS POUR L'AUTHENTIFICATION
# ============================================================

class UserPublicSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour renvoyer les informations publiques d'un utilisateur
    (Sans le mot de passe)
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_display', 
                  'speciality', 'phone', 'date_of_birth', 'is_active', 
                  'created_at']
        read_only_fields = ['id', 'created_at', 'is_active']


class RegisterSerializer(serializers.Serializer):
    """
    Sérialiseur pour l'inscription d'un nouvel utilisateur
    Valide les données et crée l'utilisateur
    """
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
        """Vérifier que le nom d'utilisateur n'existe pas déjà"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value
    
    def validate_email(self, value):
        """Vérifier que l'email n'existe pas déjà"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
    def validate(self, data):
        """Validation croisée - Vérifier que les mots de passe correspondent"""
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                'password_confirmation': 'Les mots de passe ne correspondent pas.'
            })
        return data
    
    def create(self, validated_data):
        """Créer l'utilisateur avec les données validées"""
        validated_data.pop('password_confirmation')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Sérialiseur pour la connexion
    Valide les identifiants
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


# ============================================================
# SÉRIALISEURS POUR LES GROSSESSES
# ============================================================

class PregnancySerializer(serializers.ModelSerializer):
    """Sérialiseur pour une grossesse"""
    patient_name = serializers.CharField(source='patient.username', read_only=True)
    patient_id = serializers.IntegerField(source='patient.id', read_only=True)
    
    class Meta:
        model = Pregnancy
        fields = [
            'id', 'patient', 'patient_name', 'patient_id',
            'start_date', 'expected_delivery_date', 'is_active',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PregnancyCreateSerializer(serializers.ModelSerializer):
    """Sérialiseur pour créer une grossesse"""
    class Meta:
        model = Pregnancy
        fields = ['start_date', 'expected_delivery_date', 'notes']


# ============================================================
# SÉRIALISEURS POUR LES RENDEZ-VOUS
# ============================================================

class AppointmentSerializer(serializers.ModelSerializer):
    """Sérialiseur pour un rendez-vous"""
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
    """Sérialiseur pour créer un rendez-vous"""
    class Meta:
        model = Appointment
        fields = ['caregiver', 'pregnancy', 'date_time', 'duration_minutes', 'reason']


# ============================================================
# SÉRIALISEURS POUR LES CONSULTATIONS
# ============================================================

class ConsultationSerializer(serializers.ModelSerializer):
    """Sérialiseur pour une consultation"""
    patient_name = serializers.CharField(source='appointment.patient.username', read_only=True)
    caregiver_name = serializers.CharField(source='appointment.caregiver.username', read_only=True)
    
    class Meta:
        model = Consultation
        fields = [
            'id', 'appointment', 'patient_name', 'caregiver_name',
            'consultation_date', 'report', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'consultation_date', 'created_at', 'updated_at']


# ============================================================
# SÉRIALISEURS POUR LES EXAMENS MÉDICAUX
# ============================================================

class MedicalExamSerializer(serializers.ModelSerializer):
    """Sérialiseur pour un examen médical"""
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
    """Sérialiseur pour les constantes médicales"""
    class Meta:
        model = VitalSign
        fields = [
            'id', 'consultation', 'weight_kg', 'blood_pressure_systolic',
            'blood_pressure_diastolic', 'uterine_height', 'fetal_heart_rate',
            'observations', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============================================================
# SÉRIALISEURS POUR LES ALERTES
# ============================================================

class AlertSerializer(serializers.ModelSerializer):
    """Sérialiseur pour une alerte médicale"""
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
    """Sérialiseur pour le calendrier de suivi"""
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
    """Sérialiseur pour un message"""
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
    """Sérialiseur pour les horaires d'un médecin"""
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