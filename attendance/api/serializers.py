from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Attendance, LeaveModel
from django.utils import timezone

User = get_user_model()


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ('attend_date', 'attend_time')

    def create(self, validated_data):
        now = timezone.now()
        date, time = now.date(), now.time()
        instance = Attendance.objects.create(**validated_data, attend_date=date, attend_time=time)
        return instance


class LeaveModelSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LeaveModel
        fields = "__all__"

    def create(self, validated_data):
        employee = self.context.get("request").user.employee
        instance = self.Meta.model(**validated_data, employee=employee)
        instance.save()
        return instance

