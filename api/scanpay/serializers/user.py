from rest_framework import serializers
from user.models import UserLogin

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = ['id', 'device_token', 'outlet']
