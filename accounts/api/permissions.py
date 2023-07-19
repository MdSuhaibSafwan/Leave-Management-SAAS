from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import ObjectDoesNotExist

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


class EmployeeViewSetPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        try:
            company = request.user.company

        except ObjectDoesNotExist as e:
            print(e)
            # try:
            #     employee = request.user.employee
            # except ObjectDoesNotExist as e:
            #     print(e)
            #     return False
            return True

    def has_object_permission(self, request, views, instance):
        return (request.method in SAFE_METHODS) or (instance.company.user == request.user)