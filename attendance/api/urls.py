from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import AttendanceModelViewSet, LeaveModelModelViewSet

router = DefaultRouter()
router.register("attendance", AttendanceModelViewSet, basename="user")
router.register("leave", LeaveModelModelViewSet, basename="company")

urlpatterns = [
   
] + router.urls
