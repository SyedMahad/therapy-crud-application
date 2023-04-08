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
    user = UserSerializer(read_only=True)
    user_email = serializers.CharField(write_only=True, source='user.email')

    class Meta:
        model = Counselor
        fields = ['id', 'user', 'user_email', 'is_active']

    def create(self, validated_data):
        user_email = validated_data.pop('user')['email']
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'user_email': f'User with email {user_email} not found'})

        counselor = Counselor.objects.create(user=user, **validated_data)

        return counselor

    def update(self, instance, validated_data):
        user_email = validated_data.pop('user')['email']
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'user_email': f'User with email {user_email} not found'})

        instance.user = user
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        return instance

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        message = f'Counselor with id {instance.id} has been deleted successfully.'

        return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)

