from rest_framework import permissions
from translations.models import Translation


class HasTranslationModelPermission(permissions.BasePermission):
    """Checks whether user is able to retrieve/update model"""
    message = 'You are not allowed to retrieve/update this Translation'

    def has_object_permission(self, request, view, obj):
        return any([(obj.state in Translation.ROLES_TO_AVAILABLE_STATES[role]) for role in request.user.roles])