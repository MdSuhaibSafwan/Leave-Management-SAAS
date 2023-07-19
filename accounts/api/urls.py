from django.urls import path, include

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), ),
    
]
