from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Company, Employee, CompanyGroup
from ..utils import create_user_from_validated_data
from django.contrib.auth.models import Permission

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def validate(self, values):
        ps1 = values.get("password1")
        ps2 = values.get("password2")

        if ps1 != ps2:
            raise serializers.ValidationError("Password mismatched") 

        return super().validate(values)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    groups = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()
    is_superuser = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()

    class Meta:
        model = User
        exclude = ["password"]

    def get_groups(self, instance):
        qs  = instance.groups.all()
        return qs.values()

    def get_user_permissions(self, instance):
        qs = instance.user_permissions.all()
        return qs.values()


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        fields = ["password", "new_password", "confirm_password"]

    def create(self, validated_data):
        user = self.context.get("request").user
        user.set_password(validated_data.get("password"))
        user.save()
        return user

    def validate_password(self, value):
        user = self.context.get("request").user
        return user.check_password(value)

    def validate(self, values):
        ps1 = values.get("new_password")
        ps2 = values.get("confirm_password")

        if ps1 != ps2:
            raise serializers.ValidationError("Password mismatched") 

        return super().validate(values)



class EmployeeCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    user = serializers.StringRelatedField()
    company = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        user = create_user_from_validated_data(validated_data)
        validated_data["user"] = user
        return Employee.objects.create(**validated_data)

    
class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    company = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = "__all__"


class CompanyCreateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    leaves = serializers.CharField()

    class Meta:
        model = Company
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        user = create_user_from_validated_data(validated_data)
        instance = Company.objects.create(**validated_data, user=user)
        print("Created \n\n", instance)
        return instance


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"



class PermissionHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Permission
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = "__all__"



class CompanyGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.HyperlinkedRelatedField(many=True, view_name="permissions-detail", read_only=True)

    class Meta:
        model = CompanyGroup
        fields = "__all__"

