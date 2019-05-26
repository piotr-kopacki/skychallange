from rest_framework import permissions

from .models import Exam


class ExamPermission(permissions.BasePermission):
    """Custom exam permissions"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.examiner == request.user


class TaskPermission(permissions.BasePermission):
    """Custom task permissions"""

    def has_permission(self, request, view):
        """Only examiners can create tasks for their exams."""
        if request.method == "POST":
            exams = Exam.objects.filter(pk=request.data.get("exam", -1))
            if exams.exists():
                return exams.first().examiner == request.user
        return True

    def has_object_permission(self, request, view, obj):
        """Only examiners can edit tasks. Examinees can only create answers for tasks."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.exam.archived_on:
            return False
        if (
            request.method == "PATCH"
            and request.user == obj.exam.examinee
            and request.user != obj.exam.examiner
        ):
            return len(request.data) == 1 and list(request.data)[0] == "answer"
        return obj.exam.examiner == request.user
