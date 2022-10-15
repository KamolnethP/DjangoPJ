
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




class Metadata(models.Model):
    D_TypeID = models.CharField(max_length=3)
    D_GroupID = models.CharField(max_length=3, null=True)
    D_MetadataID = models.AutoField(primary_key=True)
    D_DATE = models.DateField(auto_now_add=True)
    D_TIME = models.TimeField(auto_now_add=True)
    D_PROVINCE = models.IntegerField()
    fileName = models.CharField(max_length=255)
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dataname} {self.__all__}"



class MetadataGroup(models.Model):
    typeID = models.AutoField(primary_key=True)
    typeName = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.dataname} {self.groupID}"



class DataSetGroup(models.Model):
    groupID = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.dataname} {self.groupID}"



class AgencyDataDetail(models.Model):
    data_resource = models.CharField(max_length=255)
    dataID = models.AutoField(primary_key=True)
    access_level = models.CharField(max_length=10)
    data_type = models.CharField(max_length=100)
    dataname = models.CharField(max_length=255)
    data_format = models.CharField(max_length=10)
    objective = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dataname} {self.dataID}"




class Request(models.Model):
    agency = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    dataname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    requestID = models.AutoField(primary_key=True)
    objective = models.CharField(max_length=255)
    

    def __str__(self):
        return f"{self.dataname} {self.requestID}"



class RequestDetail(models.Model):
    dataName = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    dataID = models.CharField(max_length=50)
    detailID = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.dataname} {self.detailID}"



class RequestReturn(models.Model):
    userID = models.CharField(max_length=50)
    agency = models.CharField(max_length=255)
    dataName = models.CharField(max_length=255)
    dataID = models.CharField(max_length=50)
    data_resource = models.CharField(max_length=255)
    groupName = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.dataname} {self.dataName}"



class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=2)
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    geography_id = models.IntegerField()



