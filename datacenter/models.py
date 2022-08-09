
from django.db import models
from django.contrib.auth.models import AbstractUser


class AgencyRegister(AbstractUser):
    agency = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    username = None
    password = models.CharField(max_length=255)
    userID = models.AutoField(primary_key=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Request(models.Model):
    agency = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    dataname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    requestID = models.AutoField(primary_key=True)
    objective = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.dataname} {self.requestID}"