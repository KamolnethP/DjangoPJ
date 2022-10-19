from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import AgencyRegister,File,Request,Metadata,DataSetGroup,MetadataGroup,Province
from django.utils import encoding

class DatacenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencyRegister
        fields = ['agency', 'first_name', 'last_name', 'email', 'username', 'password', 'userID']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"
    
class FileSerializer(serializers.Serializer):
    def create(self, validated_data):
        files = self.context['files']
        data = self.context['data']
        print("==========")
        print(data)
        dataName = encoding.smart_str(data['dataName'],encoding='utf-8', strings_only=False, errors='strict')
        metadata = Metadata.objects.create( 
            metadataGroupId=data['metadataGroupId'],
            dataSetGroupId=data['dataSetGroupId'],
            fileName=data['fileName'],
            provinceId=data['provinceId'],
            dataName=dataName,
            description=data['description']
         ,**validated_data)
        for file in files:
            File.objects.create( metadata=metadata ,file=file)
        return metadata

    class Meta:
        model = Metadata
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['code','name_th','name_en']


class DataSetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSetGroup 
        fields = "__all__"


class MetadataGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataGroup 
        fields = "__all__"

