from rest_framework import serializers
from django.contrib.auth import get_user_model

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
