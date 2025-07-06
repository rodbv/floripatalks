# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    avatar = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.email or self.username
