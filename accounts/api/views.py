from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .permissions import (
    UserViewSetPermission, EmployeeViewSetPermission, CompanyViewSetPermission,
    GrantEmployeePermission, 
    PermissionViewSetPermission,
)
from .serializers import (
    UserRegisterSerializer, UserSerializer, CompanySerializer, EmployeeSerializer,
    EmployeeCreateSerializer, CompanyCreateSerializer, 
    CompanyGroupSerializer, CompanyGroupCreateSerializer,
    ChangePasswordSerializer, 
    PermissionSerializer,
)
from rest_framework.decorators import action
from ..models import Employee, Company, CompanyGroup
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status

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

    def get_serializer(self):
        if self.action == "change_password":
            return ChangePasswordSerializer
        return super().get_serializer()

    @action(detail=False, methods=["POST", ])
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "status": "done",
            "data": serializer.data
        }
        return Response(response, status=201)

    def reset_password(self, request, *args, **kwargs):
        pass

    def deactivate_account(self, request, *args, **kwargs):
        curr_user = request.user
        curr_user.is_active = False
        curr_user.save()
        response = {"message": "account deactivated"}
        return Response(response, status=201)


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [CompanyViewSetPermission, ]

    def get_queryset(self):
        return Company.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        self.serializer_class = CompanyCreateSerializer
        return super().create(request, *args, **kwargs)


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeeViewSetPermission, ]

    def get_queryset(self):
        return Employee.objects.all()

    @action(url_path="grant-employee-permission", detail=True, methods=["POST", ], 
        permission_classes=[GrantEmployeePermission, ])
    def give_employee_permission(self, request, pk):
        employee = self.get_object()
        user = employee.user
        group = Group.objects.get(name="Employee Management")
        user.groups.add(group)
        user.save()

        resp_data = {
            "message": "permission granted"
        }

        return Response(resp_data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        
        self.serializer_class = EmployeeCreateSerializer
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        curr_user = self.request.user
        try:
            company = curr_user.company
        except ObjectDoesNotExist as e:
            print(e)
            raise ValidationError("User not authorized as Company")

        serializer.save(company=company)



class PermissionViewSet(ModelViewSet):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    permission_classes = [PermissionViewSetPermission, ]


class CompanyGroupViewSet(ModelViewSet):
    serializer_class = CompanyGroupSerializer

    def get_queryset(self):
        qs = CompanyGroup.objects.all()
        return qs

    def perform_create(self, serializer):
        print("Serializer class", )
        serializer.save()

    def get_serializer(self, *args, **kwargs):
        print(self.action)
        if self.action == "create":
            self.serializer_class = CompanyGroupCreateSerializer

        return super().get_serializer(*args, **kwargs)
