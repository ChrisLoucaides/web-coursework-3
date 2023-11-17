from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    profile_picture = models.ImageField()
    date_of_birth = models.DateField()

    
