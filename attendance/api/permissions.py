from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.core.exceptions import ObjectDoesNotExist
from ..utils import check_if_employee_or_company


class LeaveModelPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        checked = check_if_employee_or_company(request.user)
        if checked is None:
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
            if employee.user.groups.filter(name="Employee Management").exists():
                return True
            return instance.employee == employee
        
        if company is not None:
            return instance.employee.company == company
        return False



class UserApprovalPermission(BasePermission):

    def has_object_permission(self, request, view, instance):
        try:
            if request.user.company != instance.employee.company:
                return False
        except ObjectDoesNotExist:
            employee = request.user.employee
            if not employee.user.groups.filter(name="Employee Management").exists():
                return False
            return True
        return True
        

class AttendanceViewSetPermission(BasePermission):

    def has_permission(self, request, view):
        checked = check_if_employee_or_company(request)
        if checked:
            return True

        return False
