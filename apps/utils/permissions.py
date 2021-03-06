from rest_framework import permissions
from users.models import User
from rest_framework.permissions import SAFE_METHODS


def has_certain_role(user, role):
    return hasattr(user, 'roles') and role in user.roles


class IsAdmin(permissions.BasePermission):
    """
    Checks whether user is Administrator
    """
    message = 'You are not Administrator.'

    def has_permission(self, request, view):
        return has_certain_role(request.user, User.ADMIN)


class IsTranslator(permissions.BasePermission):
    """
    Checks whether user is Translator
    """
    message = 'You are not Translator.'

    def has_permission(self, request, view):
        return has_certain_role(request.user, User.ROLE_TRANSLATOR)


class IsQA(permissions.BasePermission):
    """
    Checks whether user is QA
    """
    message = 'You are not QA.'

    def has_permission(self, request, view):
        return has_certain_role(request.user, User.ROLE_QA)


class IsObjectAdmin(permissions.BasePermission):
    message = 'Only Admin can manage objects.'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or has_certain_role(request.user, User.ADMIN)

    def has_object_permission(self, request, view, obj):
        return has_certain_role(request.user, User.ADMIN)
