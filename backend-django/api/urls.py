# backend/api/urls.py
"""
Routes de l'API - Version 1
"""

from django.urls import path
from .views.auth_views import RegisterView, LoginView, LogoutView, MeView
from .views.patient_views import (
    PatientPregnancyListView, PatientPregnancyDetailView,
    PatientPregnancyLossView, PatientPregnancyCompleteView,
    PatientAppointmentListView, PatientAppointmentCancelView,
    PatientExamListView, PatientVitalSignListView,
    PatientFollowUpView, PatientAlertListView,
    PatientSymptomListView, PatientMedicalHistoryView,
    PatientReminderListView, PatientGrowthMeasurementView
)
from .views.caregiver_views import (
    CaregiverPatientListView, CaregiverPatientDetailView,
    CaregiverAppointmentListView, CaregiverAppointmentStatusView,
    CaregiverConsultationCreateView,
    CaregiverExamCreateView,
    CaregiverVitalSignCreateView,
    CaregiverAlertCreateView, CaregiverAlertListView, CaregiverAlertDetailView,
    CaregiverPatientSymptomsView, CaregiverPatientMedicalHistoryView,
    CaregiverPatientRemindersView, CaregiverPatientLossView
)
from .views.admin_views import (
    AdminUserListView, AdminUserDetailView, AdminUserRoleView,
    AdminStatsView, AdminAlertListView, AdminLogListView,
    AdminExamTypeView, AdminPregnancyStatsView, AdminLossStatsView
)
from .views.admin_settings_views import AdminSettingsView
from .views.message_views import (
    PatientMessageListView,
    CaregiverMessageListView,
    CaregiverConversationView
)
from .views.schedule_views import (
    CaregiverScheduleView,
    CaregiverAvailableSlotsView
)

urlpatterns = [
    # ============================================================
    # AUTHENTIFICATION
    # ============================================================
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/me', MeView.as_view(), name='me'),
    
    # ============================================================
    # PATIENTE - Grossesses
    # ============================================================
    path('patient/pregnancies', PatientPregnancyListView.as_view(), name='patient-pregnancies'),
    path('patient/pregnancies/<int:pk>', PatientPregnancyDetailView.as_view(), name='patient-pregnancy-detail'),
    path('patient/pregnancies/<int:pk>/loss', PatientPregnancyLossView.as_view(), name='patient-pregnancy-loss'),
    path('patient/pregnancies/<int:pk>/complete', PatientPregnancyCompleteView.as_view(), name='patient-pregnancy-complete'),
    
    # ============================================================
    # PATIENTE - Rendez-vous
    # ============================================================
    path('patient/appointments', PatientAppointmentListView.as_view(), name='patient-appointments'),
    path('patient/appointments/<int:pk>/cancel', PatientAppointmentCancelView.as_view(), name='patient-appointment-cancel'),
    
    # ============================================================
    # PATIENTE - Examens et Constantes
    # ============================================================
    path('patient/exams', PatientExamListView.as_view(), name='patient-exams'),
    path('patient/vital-signs', PatientVitalSignListView.as_view(), name='patient-vital-signs'),
    
    # ============================================================
    # PATIENTE - Suivi et Alertes
    # ============================================================
    path('patient/follow-up', PatientFollowUpView.as_view(), name='patient-follow-up'),
    path('patient/alerts', PatientAlertListView.as_view(), name='patient-alerts'),
    
    # ============================================================
    # PATIENTE - Messages
    # ============================================================
    path('patient/messages', PatientMessageListView.as_view(), name='patient-messages'),
    
    # ============================================================
    # PATIENTE - Symptômes ⭐ NOUVEAU
    # ============================================================
    path('patient/symptoms', PatientSymptomListView.as_view(), name='patient-symptoms'),
    
    # ============================================================
    # PATIENTE - Historique médical ⭐ NOUVEAU
    # ============================================================
    path('patient/medical-history', PatientMedicalHistoryView.as_view(), name='patient-medical-history'),
    
    # ============================================================
    # PATIENTE - Rappels ⭐ NOUVEAU
    # ============================================================
    path('patient/reminders', PatientReminderListView.as_view(), name='patient-reminders'),
    
    # ============================================================
    # PATIENTE - Mesures de croissance ⭐ NOUVEAU
    # ============================================================
    path('patient/pregnancies/<int:pregnancy_id>/growth', PatientGrowthMeasurementView.as_view(), name='patient-growth'),
    
    # ============================================================
    # SOIGNANT - Patients
    # ============================================================
    path('caregiver/patients', CaregiverPatientListView.as_view(), name='caregiver-patients'),
    path('caregiver/patients/<int:pk>', CaregiverPatientDetailView.as_view(), name='caregiver-patient-detail'),
    
    # ============================================================
    # SOIGNANT - Rendez-vous
    # ============================================================
    path('caregiver/appointments', CaregiverAppointmentListView.as_view(), name='caregiver-appointments'),
    path('caregiver/appointments/<int:pk>/status', CaregiverAppointmentStatusView.as_view(), name='caregiver-appointment-status'),
    
    # ============================================================
    # SOIGNANT - Consultations
    # ============================================================
    path('caregiver/consultations', CaregiverConsultationCreateView.as_view(), name='caregiver-consultations'),
    
    # ============================================================
    # SOIGNANT - Examens
    # ============================================================
    path('caregiver/exams', CaregiverExamCreateView.as_view(), name='caregiver-exams'),
    
    # ============================================================
    # SOIGNANT - Constantes
    # ============================================================
    path('caregiver/vital-signs', CaregiverVitalSignCreateView.as_view(), name='caregiver-vital-signs'),
    
    # ============================================================
    # SOIGNANT - Alertes
    # ============================================================
    path('caregiver/alerts', CaregiverAlertListView.as_view(), name='caregiver-alerts'),
    path('caregiver/alerts/<int:pk>', CaregiverAlertDetailView.as_view(), name='caregiver-alert-detail'),
    
    # ============================================================
    # SOIGNANT - Messages
    # ============================================================
    path('caregiver/messages', CaregiverMessageListView.as_view(), name='caregiver-messages'),
    path('caregiver/messages/<int:patient_id>', CaregiverConversationView.as_view(), name='caregiver-conversation'),
    
    # ============================================================
    # SOIGNANT - Horaires
    # ============================================================
    path('caregiver/schedule', CaregiverScheduleView.as_view(), name='caregiver-schedule'),
    path('caregiver/slots', CaregiverAvailableSlotsView.as_view(), name='caregiver-slots'),
    
    # ============================================================
    # SOIGNANT - Symptômes patiente ⭐ NOUVEAU
    # ============================================================
    path('caregiver/patients/<int:pk>/symptoms', CaregiverPatientSymptomsView.as_view(), name='caregiver-patient-symptoms'),
    
    # ============================================================
    # SOIGNANT - Historique patiente ⭐ NOUVEAU
    # ============================================================
    path('caregiver/patients/<int:pk>/medical-history', CaregiverPatientMedicalHistoryView.as_view(), name='caregiver-patient-medical-history'),
    
    # ============================================================
    # SOIGNANT - Rappels patiente ⭐ NOUVEAU
    # ============================================================
    path('caregiver/patients/<int:pk>/reminders', CaregiverPatientRemindersView.as_view(), name='caregiver-patient-reminders'),
    
    # ============================================================
    # SOIGNANT - Perte de grossesse ⭐ NOUVEAU
    # ============================================================
    path('caregiver/patients/<int:pk>/loss', CaregiverPatientLossView.as_view(), name='caregiver-patient-loss'),
    
    # ============================================================
    # ADMINISTRATEUR - Utilisateurs
    # ============================================================
    path('admin/users', AdminUserListView.as_view(), name='admin-users'),
    path('admin/users/<int:pk>', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:pk>/role', AdminUserRoleView.as_view(), name='admin-user-role'),
    
    # ============================================================
    # ADMINISTRATEUR - Supervision
    # ============================================================
    path('admin/stats', AdminStatsView.as_view(), name='admin-stats'),
    path('admin/stats/pregnancies', AdminPregnancyStatsView.as_view(), name='admin-pregnancy-stats'),
    path('admin/stats/losses', AdminLossStatsView.as_view(), name='admin-loss-stats'),
    path('admin/alerts', AdminAlertListView.as_view(), name='admin-alerts'),
    path('admin/logs', AdminLogListView.as_view(), name='admin-logs'),
    path('admin/exam-types', AdminExamTypeView.as_view(), name='admin-exam-types'),
    path('admin/settings', AdminSettingsView.as_view(), name='admin-settings'),
]