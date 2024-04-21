# accounts/serializers.py
from rest_framework import serializers
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']

class UserSerializer(serializers.ModelSerializer):
    invited_users = SimpleUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'referrer', 'invited_users']

class AuthRequestSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

class VerifyCodeSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    code = serializers.CharField(max_length=4)

class ActivateInviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)