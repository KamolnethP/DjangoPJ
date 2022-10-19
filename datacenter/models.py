
from django.db import models
from django.contrib.auth.models import AbstractUser


class AgencyRegister(AbstractUser):
    agencyId = models.IntegerField(null=True)
    email = models.CharField(max_length=255, unique=True)
    username = None
    password = models.CharField(max_length=255)
    userID = models.AutoField(primary_key=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Agency(models.Model):
    agencyId = models.AutoField(primary_key=True)
    agencyName = models.CharField(max_length=255)

    def __str__(self):
        return self.__all__

class Metadata(models.Model):
    metadataGroupId = models.CharField(max_length=3)
    dataSetGroupId = models.CharField(max_length=3, null=True)
    metadataId = models.AutoField(primary_key=True)
    updateDate = models.DateField(auto_now_add=True)
    updateTime = models.TimeField(auto_now_add=True)
    provinceId = models.IntegerField()
    fileName = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    dataName = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    agencyId = models.IntegerField(null=True)

    def __str__(self):
        return self.__all__

class File(models.Model):
    metadata = models.ForeignKey(Metadata, related_name="file", on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False)
    fileName = models.CharField(null=True, max_length=255)

    def __str__(self):
        return self.__all__


class MetadataGroup(models.Model):
    metadataGroupId = models.AutoField(primary_key=True)
    metadataGroupName = models.CharField(max_length=100) 

    def __str__(self):
        return self.__all__



class DataSetGroup(models.Model):
    dataSetGroupId = models.AutoField(primary_key=True)
    dataSetGroupName = models.CharField(max_length=100) 

    def __str__(self):
        return self.__all__



class AgencyDataDetail(models.Model):
    data_resource = models.CharField(max_length=255)
    dataID = models.AutoField(primary_key=True)
    data_type = models.CharField(max_length=100)
    dataname = models.CharField(max_length=255)
    data_format = models.CharField(max_length=10)
    objective = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.__all__




class Request(models.Model):
    agency = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    dataname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    requestID = models.AutoField(primary_key=True)
    objective = models.CharField(max_length=255)
    

    def __str__(self):
        return self.__all__



class RequestDetail(models.Model):
    dataName = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    dataID = models.CharField(max_length=50)
    detailID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.__all__



class RequestReturn(models.Model):
    userID = models.CharField(max_length=50)
    agency = models.CharField(max_length=255)
    dataName = models.CharField(max_length=255)
    dataID = models.CharField(max_length=50)
    data_resource = models.CharField(max_length=255)
    groupName = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.__all__



class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=2)
    name_th = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    geography_id = models.IntegerField()

    def __str__(self):
        return self.__all__



