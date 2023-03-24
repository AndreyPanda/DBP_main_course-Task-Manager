from django.db import models


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
    date_of_creation = models.DateTimeField()
    date_of_change = models.DateTimeField()
    deadline = models.DateField()
    state = models.CharField(
        max_length=255, default=States.NEW_TASK, choices=States.choices
    )
    priority = models.CharField(
        max_length=255, default=Priority.MEDIUM, choices=Priority.choices
    )
