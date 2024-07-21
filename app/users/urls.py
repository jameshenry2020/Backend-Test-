from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationEndpoint


urlpatterns =[
    path('signup', UserRegistrationEndpoint.as_view()),
    path('login', TokenObtainPairView.as_view()),
    path('refresh/token', TokenRefreshView.as_view())
]