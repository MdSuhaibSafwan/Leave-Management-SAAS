from .serializers import LeaveModelSerializer, AttendanceSerializer
from ..models import Attendance, LeaveModel
from rest_framework.viewsets import ModelViewSet
from .permissions import LeaveModelPermission
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist


class AttendanceModelViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class LeaveModelModelViewSet(ModelViewSet):
    queryset = LeaveModel.objects.all()
    serializer_class = LeaveModelSerializer
    permission_classes = [LeaveModelPermission, ]

    @action(detail=True, url_path="approve", methods=["POST", "GET"])
    def approve_leave(self, request, pk=None, *args, **kwargs):
        try:
            leave_model = LeaveModel.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            raise ValidationError(e)
        employee = leave_model.employee

        if request.user.company != employee.company:
            raise ValidationError("User not in the company")
        
        leave_model.approved = True
        leave_model.save()

        data = {"approved": True}
        return Response(data, status=201)


