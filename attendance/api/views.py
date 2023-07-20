from .serializers import LeaveModelSerializer, AttendanceSerializer
from ..models import Attendance, LeaveModel
from rest_framework.viewsets import ModelViewSet
from .permissions import LeaveModelPermission, UserApprovalPermission, AttendanceViewSetPermission
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class AttendanceModelViewSet(ModelViewSet):
    # queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AttendanceViewSetPermission, ]

    def get_queryset(self):
        user = self.request.user
        qs = Attendance.objects.filter(
            Q(employee__user=user) | Q(employee__company__user=user)
        )
        # if user is company then employee_user will be empty
        # else user is employee then only employee__user will run.
        return qs

class LeaveModelModelViewSet(ModelViewSet):
    serializer_class = LeaveModelSerializer
    permission_classes = [LeaveModelPermission, ]

    def get_queryset(self):
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
        
        return qs

    @action(detail=True, url_path="approve", methods=["POST", ], 
        permission_classes=[UserApprovalPermission])
    def approve_leave(self, request, pk=None, *args, **kwargs):
        leave_instance = self.get_object()
        leave_instance.approved = True
        leave_instance.save()

        data = {"approved": True}
        return Response(data, status=status.HTTP_200_OK)
