from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Patient, Counselor, Appointment


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class CounselorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Counselor
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'counselor', 'appointment_date', 'is_active']
        read_only_fields = ['is_active']
