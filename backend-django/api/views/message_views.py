"""
Vues pour la messagerie - Patient et Médecin
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from ..models import User, Message, Pregnancy
from ..serializers import MessageSerializer
from ..permissions import IsPatient, IsCaregiver


class PatientMessageListView(APIView):
    """
    GET /api/v1/patient/messages - Messages de la patiente
    POST /api/v1/patient/messages - Envoyer un message à son médecin
    """
    permission_classes = [IsAuthenticated, IsPatient]

    @extend_schema(
        summary="Liste des messages de la patiente",
        tags=["Patiente - Messages"]
    )
    def get(self, request):
        try:
            # Récupérer les messages reçus et envoyés
            received = Message.objects.filter(recipient=request.user)
            sent = Message.objects.filter(sender=request.user)
            
            # Marquer comme lus
            received.filter(is_read=False).update(is_read=True)
            
            messages = (received | sent).order_by('-created_at')
            
            return Response({
                'message': 'Messages récupérés.',
                'data': MessageSerializer(messages, many=True).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Erreur get messages patient: {e}")
            return Response({
                'message': 'Erreur lors de la récupération des messages.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Envoyer un message à son médecin",
        tags=["Patiente - Messages"]
    )
    def post(self, request):
        try:
            # Vérifier que le médecin existe
            doctor_id = request.data.get('recipient_id')
            if not doctor_id:
                return Response({
                    'message': 'recipient_id est requis.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                doctor = User.objects.get(id=doctor_id, role='SOIGNANT')
            except User.DoesNotExist:
                return Response({
                    'message': 'Médecin non trouvé.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            content = request.data.get('content')
            if not content:
                return Response({
                    'message': 'Le contenu du message est requis.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            message = Message.objects.create(
                sender=request.user,
                recipient=doctor,
                content=content,
                pregnancy_id=request.data.get('pregnancy_id')
            )
            
            return Response({
                'message': 'Message envoyé avec succès.',
                'data': MessageSerializer(message).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ Erreur post message patient: {e}")
            return Response({
                'message': 'Erreur lors de l\'envoi du message.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CaregiverMessageListView(APIView):
    """
    GET /api/v1/caregiver/messages - Messages du médecin (conversations groupées)
    POST /api/v1/caregiver/messages - Envoyer un message à une patiente
    """
    permission_classes = [IsAuthenticated, IsCaregiver]

    @extend_schema(
        summary="Liste des conversations du médecin",
        tags=["Soignant - Messages"]
    )
    def get(self, request):
        try:
            # Récupérer tous les messages du médecin
            received = Message.objects.filter(recipient=request.user)
            sent = Message.objects.filter(sender=request.user)
            all_messages = (received | sent).order_by('-created_at')
            
            # Grouper par patiente
            conversations = {}
            for msg in all_messages:
                other_user = msg.sender if msg.sender != request.user else msg.recipient
                if other_user.role == 'PATIENTE':
                    key = other_user.id
                    if key not in conversations:
                        conversations[key] = {
                            'patient_id': other_user.id,
                            'patient_name': other_user.username,
                            'patient_email': other_user.email,
                            'last_message': msg.content,
                            'last_message_date': msg.created_at,
                            'unread': msg.recipient == request.user and not msg.is_read,
                            'messages': []
                        }
                    conversations[key]['messages'].append({
                        'id': msg.id,
                        'sender': 'me' if msg.sender == request.user else 'patient',
                        'content': msg.content,
                        'created_at': msg.created_at
                    })
            
            # Marquer comme lus
            received.filter(is_read=False).update(is_read=True)
            
            # Convertir en liste
            result = list(conversations.values())
            
            return Response({
                'message': 'Conversations récupérées.',
                'data': result
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Erreur get conversations médecin: {e}")
            return Response({
                'message': 'Erreur lors de la récupération des conversations.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Envoyer un message à une patiente",
        tags=["Soignant - Messages"]
    )
    def post(self, request):
        try:
            patient_id = request.data.get('recipient_id')
            if not patient_id:
                return Response({
                    'message': 'recipient_id est requis.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                patient = User.objects.get(id=patient_id, role='PATIENTE')
            except User.DoesNotExist:
                return Response({
                    'message': 'Patiente non trouvée.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            content = request.data.get('content')
            if not content:
                return Response({
                    'message': 'Le contenu du message est requis.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            message = Message.objects.create(
                sender=request.user,
                recipient=patient,
                content=content
            )
            
            return Response({
                'message': 'Message envoyé avec succès.',
                'data': MessageSerializer(message).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"❌ Erreur post message médecin: {e}")
            return Response({
                'message': 'Erreur lors de l\'envoi du message.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CaregiverConversationView(APIView):
    """
    GET /api/v1/caregiver/messages/<patient_id> - Conversation avec une patiente
    """
    permission_classes = [IsAuthenticated, IsCaregiver]

    @extend_schema(
        summary="Conversation avec une patiente",
        tags=["Soignant - Messages"]
    )
    def get(self, request, patient_id):
        try:
            try:
                patient = User.objects.get(id=patient_id, role='PATIENTE')
            except User.DoesNotExist:
                return Response({
                    'message': 'Patiente non trouvée.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Récupérer tous les messages entre le médecin et la patiente
            messages = Message.objects.filter(
                sender__in=[request.user, patient],
                recipient__in=[request.user, patient]
            ).order_by('created_at')
            
            # Marquer comme lus
            messages.filter(recipient=request.user, is_read=False).update(is_read=True)
            
            # Formater les messages
            result = []
            for msg in messages:
                result.append({
                    'id': msg.id,
                    'sender': 'me' if msg.sender == request.user else 'patient',
                    'sender_name': msg.sender.username,
                    'content': msg.content,
                    'created_at': msg.created_at,
                    'is_read': msg.is_read
                })
            
            return Response({
                'message': 'Conversation récupérée.',
                'data': result
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ Erreur get conversation: {e}")
            return Response({
                'message': 'Erreur lors de la récupération de la conversation.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)