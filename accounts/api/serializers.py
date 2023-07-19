from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Company, Employee

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

    def create(self, **validated_data):
        instance = super().create(validated_data)
        password = validated_data.get("password1")
        instance.set_password(password)
        instance.save()


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    groups = serializers.SerializerMethodField()
    user_permissions = serializers.SerializerMethodField()
    is_superuser = serializers.ReadOnlyField()
    last_login = serializers.ReadOnlyField()

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password", ]

    def get_groups(self, instance):
        qs  = instance.groups.all()
        return qs.values()

    def get_user_permissions(self, instance):
        qs = instance.user_permissions.all()
        return qs.values()


class EmployeeCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    user = serializers.StringRelatedField()
    comapany = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = "__all__"

    def create(self, **validated_data):
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")
        password = validated_data.get("password")
        try:
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
        except Exception as e:
            print(e)
            raise serializers.ValidationError(e)

        validated_data["user"] = user
        return super().create(validated_data)

    
class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    comapany = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"
