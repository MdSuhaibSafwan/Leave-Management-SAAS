from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import ObjectDoesNotExist


class LeaveModelPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        checked = self.check_if_employee_or_company(request, ["company", "employee"])
        if not checked:
            return False

        return True

    def has_object_permission(self, request, view, instance):
        try:
            employee = request.user.employee
        except ObjectDoesNotExist:
            employee = None

        try:
            company = request.user.company
        except ObjectDoesNotExist:
            company = None
        
        if employee is not None:
            return instance.employee == employee
        
        if company is not None:
            return instance.employee.company == company
        return False

    def check_if_employee_or_company(self, user, position_lst: list):
        for position in position_lst:
            try:
                user_pos = getattr(user, position)
                return user_pos
            except ObjectDoesNotExist:
                continue
            
            return False
