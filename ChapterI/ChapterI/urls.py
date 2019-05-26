from django.urls import include, path
from rest_framework import routers

from api.views import ExamViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r"exams", ExamViewSet, basename="exam")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [path("", include(router.urls)), path("auth/", include("rest_auth.urls"))]
