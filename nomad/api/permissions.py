from rest_framework.permissions import BasePermission


class IsNomadAdmin(BasePermission):
    """ Check if the user is an administrator """
    def has_permission(self, request, view):
        user = request.user
        return user is not None and user.is_authenticated and user.is_superuser


class IsNomadEntrepreneur(BasePermission):
    """ Check if the user is an entrepreneur """
    def has_permission(self, request, view):
        user = request.user
        return user is not None and user.is_authenticated and user.is_entrepreneur


class IsNomadCompanyUser(BasePermission):
    """ Check if the user is a company user """
    def has_permission(self, request, view):
        user = request.user
        return user is not None and user.is_authenticated and user.is_company
