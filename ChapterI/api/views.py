from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Exam, Task
from .permissions import ExamPermission, TaskPermission
from .serializers import ExamSerializer, TaskSerializer


class ExamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing exams.
    """

    permission_classes = (IsAuthenticated, ExamPermission)
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
    filterset_fields = "__all__"

    @action(detail=True, methods=["post", "patch", "put"])
    def archivize(self, request, pk=None):
        """Archivizes or dearchivizes an exam"""
        exam = self.get_object()
        if not exam.archived_on:
            exam.archived_on = timezone.now()
            exam.save()
            return Response({"status": "exam archivized"})
        else:
            exam.archived_on = None
            exam.save()
            return Response({"status": "exam dearchivized"})

    def perform_create(self, serializer):
        serializer.save(examiner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.
    """

    permission_classes = (IsAuthenticated, TaskPermission)
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filterset_fields = "__all__"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
