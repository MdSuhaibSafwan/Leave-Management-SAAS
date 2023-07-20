from .serializers import LeaveModelSerializer, AttendanceSerializer
from ..models import Attendance, LeaveModel
from rest_framework.viewsets import ModelViewSet
from .permissions import LeaveModelPermission
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist


class AttendanceModelViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class LeaveModelModelViewSet(ModelViewSet):
    serializer_class = LeaveModelSerializer
    permission_classes = [LeaveModelPermission, ]

    def get_queryset(self):
        print(self.request.user)
        try:
            employee = self.request.user.employee
            if employee.user.groups.filter(name="Employee Management").exists():
                qs = LeaveModel.objects.filter(employee__company=employee.company)
            else:
                qs = LeaveModel.objects.filter(employee=employee)

        except ObjectDoesNotExist:
            company = self.request.user.company
            qs = LeaveModel.objects.filter(employee__company=company)
        
        except Exception as e:
            raise NotFound("User not a user and not a company")
        
        print(qs)

        return qs

    # def get_object(self):

    #     self.check_permissions()

    @action(detail=True, url_path="approve", methods=["POST", ], permission_classes=[LeaveModelPermission, ])
    def approve_leave(self, request, pk=None, *args, **kwargs):
        leave_instance = self.get_object()
        employee = leave_instance.employee

        try:
            if request.user.company != employee.company:
                raise ValidationError("User not in the company")
        except ObjectDoesNotExist:
            employee = request.user.employee
            if not employee.user.groups.filter(name="Employee Management").exists():
                raise ValidationError("User not permitted to approve")
        
        leave_instance.approved = True
        leave_instance.save()

        data = {"approved": True}
        return Response(data, status=status.HTTP_200_OK)
