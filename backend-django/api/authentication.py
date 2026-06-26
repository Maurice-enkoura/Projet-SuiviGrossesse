"""
Authentification JWT personnalisée pour Django REST Framework
"""

import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


def generate_token(user):
    """
    Génère un token JWT pour un utilisateur.
    
    Args:
        user: Objet User Django
    
    Returns:
        str: Token JWT encodé
    
    Exemple d'utilisation:
        token = generate_token(user)
    """
    payload = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=settings.JWT_EXPIRES_DAYS),
        'iat': datetime.now(tz=timezone.utc),  # Issued at
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')


class JWTAuthentication(BaseAuthentication):
    """
    Authentification JWT personnalisée.
    
    Cette classe est appelée par DRF sur CHAQUE requête entrante.
    Elle lit le token JWT dans l'en-tête Authorization, le vérifie,
    et charge l'utilisateur correspondant.
    
    Fonctionnement :
    1. Lire l'en-tête Authorization: Bearer <token>
    2. Vérifier la signature du token avec PyJWT
    3. Charger l'utilisateur depuis la base de données
    4. Attacher l'utilisateur à request.user
    
    Si le token est invalide ou expiré → 401 Unauthorized
    Si pas de token → None (DRF continue vers les permissions)
    """
    
    def authenticate(self, request):
        """
        Méthode principale appelée par DRF.
        
        Retourne :
        - (user, token) → requête authentifiée, request.user = user
        - None → pas de token, requête publique possible
        - AuthenticationFailed → réponse 401 automatique
        """
        
        # 1. Lire l'en-tête Authorization
        auth_header = request.headers.get('Authorization', '')
        
        # Si pas d'en-tête Authorization ou pas de Bearer
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # Pas de token → DRF continue
        
        # Extraire le token (enlever "Bearer ")
        token = auth_header.split(' ')[1]
        
        # 2. Vérifier la signature du token avec PyJWT
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expiré. Veuillez vous reconnecter.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token invalide.')
        
        # 3. Charger l'utilisateur depuis la base de données
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('Utilisateur introuvable.')
        
        # 4. Vérifier que le compte est actif
        if not user.is_active:
            raise AuthenticationFailed('Compte désactivé.')
        
        # 5. Retourner (user, token) → DRF attache user à request.user
        return (user, token)
    
    def authenticate_header(self, request):
        """
        Indique à DRF d'envoyer WWW-Authenticate: Bearer dans les réponses 401
        """
        return 'Bearer'