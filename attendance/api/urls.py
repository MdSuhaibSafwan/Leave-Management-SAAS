from django.urls import path, include
from . import views
from .views import AttendanceModelViewSet, LeaveModelModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("attendance", AttendanceModelViewSet, basename="user")
router.register("leave", LeaveModelModelViewSet, basename="company")

urlpatterns = [
   
] + router.urls
