from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)