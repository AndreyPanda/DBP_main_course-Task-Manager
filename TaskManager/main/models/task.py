from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class States(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    class Priority(models.TextChoices):
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    date_of_creation = models.DateTimeField(null=True)
    date_of_change = models.DateTimeField(null=True)
    deadline = models.DateField(null=True)
    state = models.CharField(
        max_length=255, default=States.NEW_TASK, choices=States.choices
    )
    priority = models.CharField(
        max_length=255, default=Priority.MEDIUM, choices=Priority.choices
    )
    author = models.ForeignKey(
        User, related_name="user_author", on_delete=models.SET_NULL, null=True
    )
    executor = models.ForeignKey(
        User, related_name="user_executor", on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag)
