from django.conf import settings
from django.db import models


class Exam(models.Model):
    """Class representing an exam (created by an examinator). 
    
    Attributes:
        name: Name of an exam
        examiner: Creator of an exam.
        archived: If an exam is archived it cannot be changed.
        created_on: Date when exam was created
        archived_on: Date when exam was archived
    """

    GRADES = [(5, "A"), (4, "B"), (3, "C"), (2, "D"), (1, "F")]
    name = models.CharField(max_length=80)
    examiner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exams"
    )
    examinee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sheets"
    )
    archived_on = models.DateTimeField(blank=True, null=True)
    grade = models.CharField(max_length=1, choices=GRADES, blank=True, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """Class representing a task from an exam.
    
    Attributes:
        exam: Exam that the task is assigned to
        question: 
        content: Content of a task
    """

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="tasks")
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    points = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.question
