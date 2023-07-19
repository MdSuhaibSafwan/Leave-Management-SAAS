from django.urls import path, include
from . import views
from .views import UserViewSet, CompanyViewSet, EmployeeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("company", CompanyViewSet, basename="company")
router.register("employee", EmployeeViewSet, basename="employee")

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), ),

] + router.urls
