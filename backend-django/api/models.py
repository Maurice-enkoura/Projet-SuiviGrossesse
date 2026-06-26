"""
Modèles de données pour l'API SuiviGrossesse
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import bcrypt

# ============================================================
# GESTIONNAIRE D'UTILISATEUR PERSONNALISÉ
# ============================================================

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('account_status', 'ACTIVE')
        return self.create_user(username, email, password, **extra_fields)


class User(models.Model):
    """
    Modèle Utilisateur - Peut être PATIENTE, SOIGNANT ou ADMINISTRATEUR
    """
    # ⭐ RÔLES
    ROLE_CHOICES = [
        ('PATIENTE', 'Patiente'),
        ('SOIGNANT', 'Soignant'),
        ('ADMIN', 'Administrateur'),
    ]
    
    # ⭐ STATUTS DU COMPTE
    ACCOUNT_STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('ACTIVE', 'Actif'),
        ('REJECTED', 'Rejeté'),
        ('SUSPENDED', 'Suspendu'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    # Rôle de l'utilisateur
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENTE')
    
    # ===== STATUT DU COMPTE =====
    account_status = models.CharField(
        max_length=20, 
        choices=ACCOUNT_STATUS_CHOICES, 
        default='PENDING'
    )
    rejection_reason = models.TextField(null=True, blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    validated_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='validated_users'
    )
    
    # ===== INFORMATIONS PERSONNELLES =====
    phone = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # ===== POUR LES SOIGNANTS UNIQUEMENT =====
    speciality = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)  # Numéro d'ordre
    diploma_file = models.FileField(upload_to='diplomas/', null=True, blank=True)
    license_file = models.FileField(upload_to='licenses/', null=True, blank=True)
    id_card_file = models.FileField(upload_to='id_cards/', null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    hospital_affiliation = models.CharField(max_length=255, null=True, blank=True)
    
    # ===== POUR LES PATIENTES UNIQUEMENT =====
    is_pregnant = models.BooleanField(default=False)
    pregnancy_confirmation_date = models.DateField(null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    gynecologist_name = models.CharField(max_length=255, null=True, blank=True)
    
    # ===== DATES =====
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    # Attributs requis par Django
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    class Meta:
        managed = True
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['account_status']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def set_password(self, raw_password):
        """Hasher le mot de passe"""
        try:
            self.password = make_password(raw_password, hasher='bcrypt')
        except ValueError:
            self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Vérifier un mot de passe hashé"""
        try:
            return check_password(raw_password, self.password)
        except:
            return False


# ============================================================
# MODÈLES EXISTANTS (Pregnancy, Appointment, Consultation, etc.)
# ============================================================

class Pregnancy(models.Model):
    """
    Grossesse d'une patiente
    """
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='pregnancies'
    )
    start_date = models.DateField(help_text="Date des dernières règles (DDR)")
    expected_delivery_date = models.DateField(help_text="Date prévue d'accouchement (DPA)")
    is_active = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'pregnancies'
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'is_active'],
                condition=models.Q(is_active=True),
                name='unique_active_pregnancy'
            )
        ]
    
    def __str__(self):
        return f"Grossesse de {self.patient.username}"


class Appointment(models.Model):
    """
    Rendez-vous entre une patiente et un soignant
    """
    STATUS_CHOICES = [
        ('SCHEDULED', 'Programmé'),
        ('CONFIRMED', 'Confirmé'),
        ('COMPLETED', 'Effectué'),
        ('CANCELLED', 'Annulé'),
    ]
    
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='appointments_as_patient'
    )
    caregiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='appointments_as_caregiver'
    )
    pregnancy = models.ForeignKey(
        Pregnancy, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    date_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'appointments'
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['caregiver']),
            models.Index(fields=['status']),
            models.Index(fields=['date_time']),
        ]
    
    def __str__(self):
        return f"RDV {self.patient.username} le {self.date_time}"


class Consultation(models.Model):
    """
    Consultation médicale
    """
    appointment = models.ForeignKey(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='consultations'
    )
    consultation_date = models.DateField(auto_now_add=True)
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'consultations'
        indexes = [
            models.Index(fields=['appointment']),
        ]
    
    def __str__(self):
        return f"Consultation du {self.consultation_date}"


class MedicalExam(models.Model):
    """
    Examen médical
    """
    EXAM_TYPES = [
        ('BLOOD', 'Prise de sang'),
        ('URINE', 'Analyse d\'urine'),
        ('ULTRASOUND', 'Échographie'),
        ('BLOOD_PRESSURE', 'Tension artérielle'),
        ('WEIGHT', 'Poids'),
        ('OTHER', 'Autre'),
    ]
    
    consultation = models.ForeignKey(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name='exams'
    )
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    exam_date = models.DateField(auto_now_add=True)
    result_summary = models.TextField()
    details = models.JSONField(null=True, blank=True)
    is_abnormal = models.BooleanField(default=False)
    file_attachment = models.FileField(upload_to='exams/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'medical_exams'
        indexes = [
            models.Index(fields=['consultation']),
            models.Index(fields=['exam_type']),
            models.Index(fields=['is_abnormal']),
        ]
    
    def __str__(self):
        return f"{self.get_exam_type_display()}"


class VitalSign(models.Model):
    """
    Constantes médicales
    """
    consultation = models.ForeignKey(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name='vital_signs'
    )
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    uterine_height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fetal_heart_rate = models.IntegerField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'vital_signs'
        indexes = [
            models.Index(fields=['consultation']),
        ]
    
    def __str__(self):
        return f"Constantes - {self.consultation.appointment.patient.username}"


class Alert(models.Model):
    """
    Alerte médicale
    """
    ALERT_TYPES = [
        ('HYPERTENSION', 'Hypertension'),
        ('BLEEDING', 'Saignement'),
        ('PRETERM_RISK', 'Risque d\'accouchement prématuré'),
        ('GESTATIONAL_DIABETES', 'Diabète gestationnel'),
        ('OTHER', 'Autre'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Faible'),
        ('MEDIUM', 'Moyen'),
        ('HIGH', 'Élevé'),
        ('CRITICAL', 'Critique'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ACKNOWLEDGED', 'Accusée'),
        ('RESOLVED', 'Résolue'),
    ]
    
    consultation = models.ForeignKey(
        Consultation, 
        on_delete=models.CASCADE, 
        related_name='alerts'
    )
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    description = models.TextField()
    action_taken = models.TextField(null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'alerts'
        indexes = [
            models.Index(fields=['consultation']),
            models.Index(fields=['alert_type']),
            models.Index(fields=['severity']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.severity}"


class FollowUpSchedule(models.Model):
    """
    Calendrier de suivi
    """
    pregnancy = models.ForeignKey(
        Pregnancy, 
        on_delete=models.CASCADE, 
        related_name='follow_up_schedule'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    scheduled_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'follow_up_schedule'
        indexes = [
            models.Index(fields=['pregnancy']),
            models.Index(fields=['scheduled_date']),
            models.Index(fields=['is_completed']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_date}"


class UserCaregiver(models.Model):
    """
    Relation ManyToMany entre patientes et soignants
    """
    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='caregiver_assignments'
    )
    caregiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='patient_assignments'
    )
    is_primary = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'user_caregivers'
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['caregiver']),
            models.Index(fields=['is_primary']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'caregiver'],
                name='unique_assignment'
            )
        ]
    
    def __str__(self):
        return f"{self.patient.username} → {self.caregiver.username}"


class AuditLog(models.Model):
    """
    Journal des actions
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='audit_logs'
    )
    action = models.CharField(max_length=100)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.action}"


# ============================================================
# NOUVEAUX MODÈLES
# ============================================================

class Message(models.Model):
    """
    Message entre un médecin et une patiente
    """
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )
    pregnancy = models.ForeignKey(
        Pregnancy, 
        on_delete=models.CASCADE, 
        related_name='messages',
        null=True,
        blank=True
    )
    subject = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'messages'
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['recipient']),
            models.Index(fields=['is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Message de {self.sender.username} à {self.recipient.username}"


class DoctorSchedule(models.Model):
    """
    Horaires de consultation d'un médecin
    """
    DAY_CHOICES = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]
    
    doctor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='schedules'
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    is_working = models.BooleanField(default=True)
    morning_start = models.TimeField(null=True, blank=True)
    morning_end = models.TimeField(null=True, blank=True)
    afternoon_start = models.TimeField(null=True, blank=True)
    afternoon_end = models.TimeField(null=True, blank=True)
    slot_duration = models.IntegerField(default=30, help_text="Durée des créneaux en minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = True
        db_table = 'doctor_schedules'
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'day_of_week'],
                name='unique_doctor_day'
            )
        ]
    
    def __str__(self):
        return f"{self.doctor.username} - {self.get_day_of_week_display()}"