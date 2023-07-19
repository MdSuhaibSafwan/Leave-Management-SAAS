from rest_framework.generic import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from .permissions import UserViewSetPermission


User = get_user_model()


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserAPIViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [UserViewSetPermission, ]
    
    def get_queryset(self):
        qs = User.objects.all()
        return qs
