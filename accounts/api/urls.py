from django.urls import path, include
from . import views
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), ),

] + router.urls
