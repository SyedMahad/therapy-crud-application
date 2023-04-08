from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Patient, Counselor


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['id', 'user', 'username', 'email', 'first_name', 'last_name', 'is_active']

class CounselorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Counselor
        fields = ['id', 'user', 'username', 'email', 'first_name', 'last_name', 'is_active']

