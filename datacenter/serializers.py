from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import AgencyRegister,Request

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
    
