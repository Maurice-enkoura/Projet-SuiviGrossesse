"""
Permissions personnalisées pour l'API SuiviGrossesse
"""

from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    """Permission : L'utilisateur doit être une PATIENTE."""
    message = "Accès interdit. Rôle requis : PATIENTE."
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'PATIENTE')


class IsCaregiver(BasePermission):
    """Permission : L'utilisateur doit être un SOIGNANT."""
    message = "Accès interdit. Rôle requis : SOIGNANT."
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'SOIGNANT')


class IsAdmin(BasePermission):
    """Permission : L'utilisateur doit être un ADMINISTRATEUR."""
    message = "Accès interdit. Rôle requis : ADMINISTRATEUR."
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'ADMIN')


class IsCaregiverOrAdmin(BasePermission):
    """Permission : L'utilisateur doit être SOIGNANT ou ADMINISTRATEUR."""
    message = "Accès interdit. Rôles requis : SOIGNANT ou ADMINISTRATEUR."
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.role in ('SOIGNANT', 'ADMIN'))


class IsPatientOrCaregiver(BasePermission):
    """Permission : L'utilisateur doit être PATIENTE ou SOIGNANT."""
    message = "Accès interdit. Rôles requis : PATIENTE ou SOIGNANT."
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.role in ('PATIENTE', 'SOIGNANT'))