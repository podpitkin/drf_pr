from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import (PaymentListCreateView, ProfileView, RegisterView, UserViewSet)

app_name = UsersConfig.name


urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('payments/', PaymentListCreateView.as_view(), name='payments-list-create'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]


