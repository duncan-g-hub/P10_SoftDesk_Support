from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):

    birth_date = models.DateField(verbose_name='Date de naissance',null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)



