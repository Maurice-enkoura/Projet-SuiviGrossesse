"""
Vues pour l'authentification (inscription, connexion, déconnexion, profil)
Avec documentation Swagger (drf-spectacular)
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from ..serializers import RegisterSerializer, LoginSerializer, UserPublicSerializer
from ..authentication import generate_token
from ..models import User, AuditLog


class RegisterView(APIView):
    """
    POST /api/v1/auth/register - Inscription d'un nouvel utilisateur
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Inscription - Créer un compte",
        description="Création d'un compte utilisateur avec rôle spécifié. Retourne un token JWT.",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="Inscription réussie"),
            422: OpenApiResponse(description="Erreur de validation")
        },
        tags=["Authentification"]
    )
    def post(self, request):
        # 1. Valider les données
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Erreur de validation.',
                    'errors': serializer.errors
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # 2. Créer l'utilisateur
        user = serializer.save()
        
        # 3. Générer le token JWT
        token = generate_token(user)
        
        # 4. Journaliser l'action
        AuditLog.objects.create(
            user=user,
            action='REGISTER',
            description=f"Inscription de {user.email} avec le rôle {user.role}",
            ip_address=self.get_client_ip(request),
        )
        
        # 5. Réponse
        return Response(
            {
                'message': 'Inscription réussie.',
                'user': UserPublicSerializer(user).data,
                'token': token
            },
            status=status.HTTP_201_CREATED
        )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LoginView(APIView):
    """
    POST /api/v1/auth/login - Connexion
    Authentifie un utilisateur et retourne un token JWT.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Connexion - Obtenir un token JWT",
        description="Authentification avec email et mot de passe.",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(description="Connexion réussie"),
            401: OpenApiResponse(description="Identifiants incorrects"),
            422: OpenApiResponse(description="Erreur de validation")
        },
        tags=["Authentification"]
    )
    def post(self, request):
        # 1. Valider les données
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Erreur de validation.',
                    'errors': serializer.errors
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        data = serializer.validated_data
        
        # 2. Trouver l'utilisateur par email
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response(
                {'message': 'Identifiants incorrects.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 3. Vérifier le mot de passe
        if not user.check_password(data['password']):
            return Response(
                {'message': 'Identifiants incorrects.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 4. Vérifier que le compte est actif
        if not user.is_active:
            return Response(
                {'message': 'Compte désactivé. Contactez l\'administrateur.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 5. Générer le token JWT
        token = generate_token(user)
        
        # 6. Journaliser l'action
        AuditLog.objects.create(
            user=user,
            action='LOGIN',
            description=f"Connexion de {user.email}",
            ip_address=self.get_client_ip(request),
        )
        
        # 7. Réponse
        return Response(
            {
                'message': 'Connexion réussie.',
                'user': UserPublicSerializer(user).data,
                'token': token
            },
            status=status.HTTP_200_OK
        )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout - Déconnexion
    JWT est stateless - le client doit supprimer le token localement.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Déconnexion",
        description="Déconnexion de l'utilisateur. Supprimez le token côté client.",
        responses={
            200: OpenApiResponse(description="Déconnexion réussie"),
            401: OpenApiResponse(description="Non authentifié")
        },
        tags=["Authentification"]
    )
    def post(self, request):
        AuditLog.objects.create(
            user=request.user,
            action='LOGOUT',
            description=f"Déconnexion de {request.user.email}",
            ip_address=self.get_client_ip(request),
        )
        
        return Response(
            {
                'message': 'Déconnexion réussie. Supprimez le token côté client.'
            },
            status=status.HTTP_200_OK
        )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class MeView(APIView):
    """
    GET /api/v1/auth/me - Profil de l'utilisateur connecté
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Profil - Informations de l'utilisateur connecté",
        description="Retourne les informations de l'utilisateur authentifié.",
        responses={
            200: OpenApiResponse(description="Profil récupéré"),
            401: OpenApiResponse(description="Non authentifié")
        },
        tags=["Authentification"]
    )
    def get(self, request):
        return Response(
            {
                'message': 'Profil récupéré.',
                'user': UserPublicSerializer(request.user).data
            },
            status=status.HTTP_200_OK
        )