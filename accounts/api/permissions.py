from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import ObjectDoesNotExist


COMPANY_AUTH_PERMISSIONS = [
    'add_companygroup', 'change_companygroup', 
    'delete_companygroup', 'view_companygroup', 'add_companyposition', 
    'change_companyposition', 'delete_companyposition', 'view_companyposition', 
    'add_employee', 'change_employee', 'delete_employee', 'view_employee', 
    'add_employeeshift', 'change_employeeshift', 'delete_employeeshift', 
    'view_employeeshift', 'add_user', 'change_user', 'delete_user', 
    'view_user', 'view_attendance', 'change_leavemodel', 'view_leavemodel'
]


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


class GrantEmployeePermission(BasePermission):
    
    def has_permission(self, request, view):
        try:
            getattr(request.user, "company")
        except ObjectDoesNotExist:
            return False

        return True

    def has_object_permission(self, request, view, instance):
        curr_user_company = request.user.company
        return instance.company == curr_user_company


class PermissionViewSetPermission(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS



class CompanyGroupViewSetPermission(BasePermission):

    def has_permission(self, request, view):
        try:
            obj = request.user.company
        except ObjectDoesNotExist:
            obj = request.user.employee
        except Exception as e:
            return False
        
        return obj.user.has_perm("accounts.add_group")
