from .serializers import LeaveModelSerializer, AttendanceSerializer
from ..models import Attendance, LeaveModel
from rest_framework.viewsets import ModelViewSet
from .permissions import LeaveModelPermission
from rest_framework.response import Response
from rest_framework.decorators import action


class AttendanceModelViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class LeaveModelModelViewSet(ModelViewSet):
    queryset = LeaveModel.objects.all()
    serializer_class = LeaveModelSerializer
    permission_classes = [LeaveModelPermission, ]

    @action(detail=True, url_path="approve", methods=["POST", ])
    def approve_leave(self, request, id, **kwargs):

        data = {"approved": True}
        return Response(data, status=201)


