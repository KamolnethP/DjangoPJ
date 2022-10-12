from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import AgencyRegister,Request,Metadata,DataSetGroup,MetadataGroup,Province

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
    
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata 
        fields = "__all__"


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

