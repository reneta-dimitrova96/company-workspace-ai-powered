from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    position = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

