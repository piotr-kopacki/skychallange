from rest_framework import serializers

from .models import Exam, Task


class ExamSerializer(serializers.ModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="task-detail"
    )

    class Meta:
        model = Exam
        fields = "__all__"
        read_only_fields = ("archived_on", "examiner")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
