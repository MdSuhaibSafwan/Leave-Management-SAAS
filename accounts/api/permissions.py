from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserViewSetPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return str(request.method).upper() != "POST"

