from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    role = models.CharField(
        max_length=255, default=Roles.DEVELOPER, choices=Roles.choices
    )
    email = models.EmailField()
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
