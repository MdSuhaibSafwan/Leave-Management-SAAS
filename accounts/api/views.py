from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .permissions import UserViewSetPermission
from .serializers import (
    UserRegisterSerializer, UserSerializer, CompanySerializer, EmployeeSerializer,
    EmployeeCreateSerializer, CompanyCreateSerializer
)
from rest_framework.decorators import action
from ..models import Employee, Company
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [UserViewSetPermission, ]
    
    def get_queryset(self):
        qs = User.objects.all()
        return qs

    @action(detail=False, methods=["POST", ])
    def change_password(self, request, *args, **kwargs):
        pass

    def reset_password(self, request, *args, **kwargs):
        pass

    def deactivate_account(self, request, *args, **kwargs):
        pass


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        return Company.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        self.serializer_class = CompanyCreateSerializer
        return super().create(request, *args, **kwargs)


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all()

    def perform_create(self, serializer):
        curr_user = self.request.user
        try:
            company = curr_user.company
        except ObjectDoesNotExist as e:
            print(e)
            raise ValidationError("User not authorized as Company")

        serializer.save(company=company)

    def create(self, request, *args, **kwargs):
        self.serializer_class = EmployeeCreateSerializer
        return super().create(request, *args, **kwargs)



