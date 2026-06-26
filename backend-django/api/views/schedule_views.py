"""
Vues pour la gestion des horaires des médecins
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from datetime import datetime, timedelta

from ..models import User, DoctorSchedule
from ..serializers import DoctorScheduleSerializer
from ..permissions import IsCaregiver


class CaregiverScheduleView(APIView):
    """
    GET /api/v1/caregiver/schedule - Horaires du médecin
    POST /api/v1/caregiver/schedule - Créer/modifier les horaires
    """
    permission_classes = [IsAuthenticated, IsCaregiver]

    @extend_schema(
        summary="Récupérer les horaires du médecin",
        tags=["Soignant - Horaires"]
    )
    def get(self, request):
        try:
            schedules = DoctorSchedule.objects.filter(doctor=request.user).order_by('day_of_week')
            
            # Si aucun horaire n'existe, créer des horaires par défaut
            if not schedules.exists():
                default_schedules = []
                for day in range(5):  # Lundi à Vendredi
                    default_schedules.append({
                        'doctor': request.user.id,
                        'day_of_week': day,
                        'is_working': True,
                        'morning_start': '09:00',
                        'morning_end': '12:00',
                        'afternoon_start': '14:00',
                        'afternoon_end': '17:00',
                        'slot_duration': 30
                    })
                # Samedi (optionnel)
                default_schedules.append({
                    'doctor': request.user.id,
                    'day_of_week': 5,
                    'is_working': False,
                    'morning_start': None,
                    'morning_end': None,
                    'afternoon_start': None,
                    'afternoon_end': None,
                    'slot_duration': 30
                })
                # Dimanche (fermé)
                default_schedules.append({
                    'doctor': request.user.id,
                    'day_of_week': 6,
                    'is_working': False,
                    'morning_start': None,
                    'morning_end': None,
                    'afternoon_start': None,
                    'afternoon_end': None,
                    'slot_duration': 30
                })
                
                for schedule_data in default_schedules:
                    serializer = DoctorScheduleSerializer(data=schedule_data)
                    if serializer.is_valid():
                        serializer.save()
                
                schedules = DoctorSchedule.objects.filter(doctor=request.user).order_by('day_of_week')
            
            return Response({
                'message': 'Horaires récupérés.',
                'data': DoctorScheduleSerializer(schedules, many=True).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Erreur get schedule: {e}")
            return Response({
                'message': 'Erreur lors de la récupération des horaires.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Modifier les horaires du médecin",
        tags=["Soignant - Horaires"]
    )
    def post(self, request):
        try:
            # Supprimer les anciens horaires
            DoctorSchedule.objects.filter(doctor=request.user).delete()
            
            # Créer les nouveaux horaires
            schedules_data = request.data.get('schedules', [])
            created_schedules = []
            
            for schedule_data in schedules_data:
                serializer = DoctorScheduleSerializer(data=schedule_data)
                if serializer.is_valid():
                    serializer.save(doctor=request.user)
                    created_schedules.append(serializer.data)
            
            return Response({
                'message': 'Horaires mis à jour avec succès.',
                'data': created_schedules
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Erreur post schedule: {e}")
            return Response({
                'message': 'Erreur lors de la mise à jour des horaires.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CaregiverAvailableSlotsView(APIView):
    """
    GET /api/v1/caregiver/slots - Créneaux disponibles d'un médecin
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Récupérer les créneaux disponibles d'un médecin",
        tags=["Soignant - Horaires"]
    )
    def get(self, request):
        try:
            doctor_id = request.query_params.get('doctor_id')
            date_str = request.query_params.get('date')
            
            if not doctor_id or not date_str:
                return Response({
                    'message': 'doctor_id et date sont requis.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                doctor = User.objects.get(id=doctor_id, role='SOIGNANT')
            except User.DoesNotExist:
                return Response({
                    'message': 'Médecin non trouvé.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Récupérer les horaires du médecin pour ce jour
            date = datetime.strptime(date_str, '%Y-%m-%d')
            day_of_week = date.weekday()
            
            schedules = DoctorSchedule.objects.filter(
                doctor=doctor,
                day_of_week=day_of_week,
                is_working=True
            )
            
            if not schedules.exists():
                return Response({
                    'message': 'Aucun horaire disponible pour cette date.',
                    'data': []
                }, status=status.HTTP_200_OK)
            
            slots = []
            for schedule in schedules:
                slot_duration = schedule.slot_duration or 30
                
                # Créneaux du matin
                if schedule.morning_start and schedule.morning_end:
                    current = schedule.morning_start
                    while current < schedule.morning_end:
                        slots.append(current.strftime('%H:%M'))
                        current = (datetime.combine(datetime.today(), current) + 
                                  timedelta(minutes=slot_duration)).time()
                
                # Créneaux de l'après-midi
                if schedule.afternoon_start and schedule.afternoon_end:
                    current = schedule.afternoon_start
                    while current < schedule.afternoon_end:
                        slots.append(current.strftime('%H:%M'))
                        current = (datetime.combine(datetime.today(), current) + 
                                  timedelta(minutes=slot_duration)).time()
            
            return Response({
                'message': 'Créneaux disponibles récupérés.',
                'data': slots
            }, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response({
                'message': 'Format de date invalide. Utilisez YYYY-MM-DD.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"❌ Erreur get slots: {e}")
            return Response({
                'message': 'Erreur lors de la récupération des créneaux.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)