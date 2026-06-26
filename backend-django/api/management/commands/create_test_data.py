# backend/api/management/commands/create_test_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Crée des données de test pour le suivi de grossesse'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Création des données de test...')
        
        try:
            from api.models import User, Pregnancy, Appointment, Consultation, MedicalExam, VitalSign
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur d\'import: {e}'))
            return

        # ============================================
        # 1. CRÉER LES UTILISATEURS
        # ============================================
        
        # Patient
        patient, created = User.objects.get_or_create(
            username='patient_test',
            defaults={
                'email': 'patient@test.com',
                'role': 'PATIENTE',
                'phone': '+242 06 123 45 67',
                'is_active': True,
            }
        )
        if created:
            patient.set_password('password123')
            patient.save()
            self.stdout.write(f'✅ Patient créé: {patient.username}')
        else:
            self.stdout.write(f'ℹ️ Patient existant: {patient.username}')
            patient.set_password('password123')
            patient.save()

        # Médecin
        doctor, created = User.objects.get_or_create(
            username='dr_martin',
            defaults={
                'email': 'dr.martin@test.com',
                'role': 'SOIGNANT',
                'speciality': 'Gynécologie',
                'phone': '+242 06 111 22 33',
                'is_active': True,
            }
        )
        if created:
            doctor.set_password('doctor123')
            doctor.save()
            self.stdout.write(f'✅ Médecin créé: {doctor.username}')
        else:
            self.stdout.write(f'ℹ️ Médecin existant: {doctor.username}')
            doctor.set_password('doctor123')
            doctor.save()

        # Admin
        admin, created = User.objects.get_or_create(
            username='admin_test',
            defaults={
                'email': 'admin@test.com',
                'role': 'ADMIN',
                'is_active': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(f'✅ Admin créé: {admin.username}')
        else:
            self.stdout.write(f'ℹ️ Admin existant: {admin.username}')
            admin.set_password('admin123')
            admin.save()

        # ============================================
        # 2. CRÉER UNE GROSSESSE
        # ============================================
        
        # Supprimer les anciennes grossesses du patient
        Pregnancy.objects.filter(patient=patient).delete()
        
        start_date = datetime.now().date() - timedelta(days=84)
        expected_delivery = datetime.now().date() + timedelta(days=196)
        
        pregnancy = Pregnancy.objects.create(
            patient=patient,
            start_date=start_date,
            expected_delivery_date=expected_delivery,
            is_active=True,
            notes="Grossesse normale, suivi régulier."
        )
        self.stdout.write(f'✅ Grossesse créée (ID: {pregnancy.id})')

        # ============================================
        # 3. CRÉER DES RENDEZ-VOUS
        # ============================================
        
        appointments = [
            {
                'date_time': datetime.now() + timedelta(days=3),
                'duration_minutes': 30,
                'reason': 'Suivi de grossesse - 13ème semaine',
                'status': 'CONFIRMED',
                'notes': 'Échographie à prévoir'
            },
            {
                'date_time': datetime.now() - timedelta(days=7),
                'duration_minutes': 45,
                'reason': 'Première consultation',
                'status': 'COMPLETED',
                'notes': 'Patiente en bonne santé'
            },
            {
                'date_time': datetime.now() + timedelta(days=10),
                'duration_minutes': 30,
                'reason': 'Consultation de suivi',
                'status': 'SCHEDULED',
                'notes': 'Vérifier la prise de poids'
            }
        ]

        created_appointments = []
        for appt_data in appointments:
            appointment = Appointment.objects.create(
                patient=patient,
                caregiver=doctor,
                pregnancy=pregnancy,
                **appt_data
            )
            created_appointments.append(appointment)
            self.stdout.write(f'✅ Rendez-vous créé: {appointment.date_time.strftime("%d/%m/%Y %H:%M")}')

        # ============================================
        # 4. CRÉER DES CONSULTATIONS
        # ============================================
        
        for appt in created_appointments:
            if appt.status == 'COMPLETED':
                consultation = Consultation.objects.create(
                    appointment=appt,
                    report=f"Consultation du {appt.date_time.strftime('%d/%m/%Y')}.\n\n"
                           f"Motif: {appt.reason}\n"
                           f"Observations: Patiente en bonne santé, grossesse évolue normalement.\n"
                           f"Prochain rendez-vous dans 4 semaines."
                )
                self.stdout.write(f'✅ Consultation créée pour le rendez-vous du {appt.date_time.strftime("%d/%m/%Y")}')

        # ============================================
        # 5. CRÉER DES EXAMENS MÉDICAUX
        # ============================================
        
        consultations = Consultation.objects.all()
        for consultation in consultations:
            exams_data = [
                {
                    'exam_type': 'BLOOD',
                    'result_summary': 'Hémoglobine: 12.5 g/dL, Plaquettes: 250 000, Fer: 80 µg/dL',
                    'is_abnormal': False,
                },
                {
                    'exam_type': 'BLOOD_PRESSURE',
                    'result_summary': 'Tension: 120/80 mmHg',
                    'is_abnormal': False,
                },
            ]
            
            for exam_data in exams_data:
                exam = MedicalExam.objects.create(
                    consultation=consultation,
                    **exam_data
                )
                self.stdout.write(f'✅ Examen créé: {exam.get_exam_type_display()}')

        # ============================================
        # 6. RÉSUMÉ
        # ============================================
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Données de test créées avec succès !'))
        self.stdout.write('\n📋 RÉCAPITULATIF:')
        self.stdout.write(f'   👤 Patient: {patient.username} ({patient.role})')
        self.stdout.write(f'   👨‍⚕️ Médecin: {doctor.username} ({doctor.speciality})')
        self.stdout.write(f'   🤰 Grossesse: Active')
        self.stdout.write(f'   📅 Rendez-vous: {Appointment.objects.filter(patient=patient).count()}')
        self.stdout.write(f'   🩺 Consultations: {Consultation.objects.filter(appointment__patient=patient).count()}')
        self.stdout.write(f'   🔬 Examens: {MedicalExam.objects.filter(consultation__appointment__patient=patient).count()}')
        
        self.stdout.write('\n🔑 IDENTIFIANTS DE TEST:')
        self.stdout.write(f'   Patient: patient@test.com / password123')
        self.stdout.write(f'   Médecin: dr.martin@test.com / doctor123')
        self.stdout.write(f'   Admin: admin@test.com / admin123')
        
        self.stdout.write('\n📱 POUR LE FRONTEND:')
        self.stdout.write('   Connexion avec patient@test.com / password123')
        self.stdout.write('   URL: http://localhost:5173/login')