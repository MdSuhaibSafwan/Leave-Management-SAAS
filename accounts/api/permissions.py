from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserViewSetPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return str(request.method).upper() not in ["POST", "DELETE"]

    def has_object_permission(self, request, views, instance):
        return (request.method in SAFE_METHODS) or (instance == request.user)


class CompanyViewSetPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_superuser

