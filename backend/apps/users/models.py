from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    @property
    def is_phystech_student(self):
        return self.email.lower().endswith("@phystech.edu")

