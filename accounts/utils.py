from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def create_user_from_validated_data(validated_data):
    first_name = validated_data.pop("first_name")
    last_name = validated_data.pop("last_name")
    email = validated_data.pop("email")
    password = validated_data.pop("password")

    try:
        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, )
    except Exception as e:
        print(e)
        raise serializers.ValidationError(e)

    return user

