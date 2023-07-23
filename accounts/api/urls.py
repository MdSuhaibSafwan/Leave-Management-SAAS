from django.urls import path, include
from . import views
from .views import (
    UserViewSet, CompanyViewSet, EmployeeViewSet, 
    CompanyGroupViewSet, PermissionViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("company", CompanyViewSet, basename="company")
router.register("employee", EmployeeViewSet, basename="employee")
router.register("company-group", CompanyGroupViewSet, basename="company_group")
router.register("permissions", PermissionViewSet, basename="permissions")

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), ),

] + router.urls
