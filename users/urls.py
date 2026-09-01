from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import ProfileView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", ProfileView)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
]

urlpatterns += router.urls
