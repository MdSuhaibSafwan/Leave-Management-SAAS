from rest_framework.permissions import BasePermission, SAFE_METHODS


class LeaveModelPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return True

    def has_object_permission(self, request, view, instance):
        try:
            employee = request.user.employee
        except ObjectDoesNotExist:
            return False

        try:
            return (employee == instance.employee) or (employee.company == user.company)
        except Exception as e:
            print(e)
            return False