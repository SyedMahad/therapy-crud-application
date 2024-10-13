from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db import transaction

from .models import User, Patient, Counselor, Appointment
import constants


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""

    class Meta:
        model = Patient
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class CounselorSerializer(serializers.ModelSerializer):
    """Serializer for Counselor model"""

    class Meta:
        model = Counselor
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'counselor', 'appointment_date', 'is_active']
        read_only_fields = ['is_active']    # 'is_active' field is read-only and managed by server

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'user_type')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        try:
            # Remove password2 and get user_type
            password = validated_data.pop('password')
            validated_data.pop('password2')
            user_type = validated_data.pop('user_type')

            with transaction.atomic():
                # Create the user
                user = User.objects.create_user(password=password, user_type=user_type, **validated_data)

                # No need to create Patient or Counselor objects separately since they are proxies
                if user_type == constants.USER_TYPE_PATIENT:
                    # The Patient proxy will automatically behave like a patient
                    user = Patient.objects.get(pk=user.pk)
                elif user_type == constants.USER_TYPE_COUNSELOR:
                    # The Counselor proxy will automatically behave like a counselor
                    user = Counselor.objects.get(pk=user.pk)

            return user

        except Exception as e:
            raise e


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Override the 'username' field to use 'email'
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('No user found with this email address.')

            # Update 'username' with the actual username value for token generation
            attrs['username'] = user.username

        return super().validate(attrs)
