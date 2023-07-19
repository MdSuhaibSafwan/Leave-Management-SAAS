from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Employee

User = get_user_model()


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendaces")
    attend_date = models.DateField()
    attend_time = models.TimeField()
    description = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class LeaveModel(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaves")
    leave_date = models.DateField()
    half_day = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    reason = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)