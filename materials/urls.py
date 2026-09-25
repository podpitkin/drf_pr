from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonListCreateView,
                             LessonRetrieveUpdateDestroyView, SubscriptionView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListCreateView.as_view(), name="lessons-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyView.as_view(),
        name="lessons-retrieve-update-delete",
    ),
    path("subscription/", SubscriptionView.as_view(), name="subscription"),
]

urlpatterns += router.urls

