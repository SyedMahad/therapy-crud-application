from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Patient, Counselor, Appointment
from .serializers import (
    UserSerializer,
    PatientSerializer,
    CounselorSerializer,
    AppointmentSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset to handle CRUD operations for User model"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

class PatientViewSet(viewsets.ModelViewSet):
    """Viewset to handle CRUD operations for Patient model"""

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('username', 'email', 'first_name', 'last_name', 'is_active',)

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete for Patient objects.
        Instead of actually deleting the object, set the `is_active` field to False.
        """
        instance = self.get_object()

        # Set is_active to False to deactivate the patient
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CounselorViewSet(viewsets.ModelViewSet):
    """Viewset to handle CRUD operations for Counselor model"""

    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('username', 'email', 'first_name', 'last_name', 'is_active',)

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete for Counselor objects.
        Instead of actually deleting the object, set the `is_active` field to False.
        """
        instance = self.get_object()

        # Set is_active to False to deactivate the counselor
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class AppointmentViewSet(viewsets.ModelViewSet):
    """Viewset to handle CRUD operations for Appointment model"""

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('patient', 'counselor', 'appointment_date', 'is_active',)

    def get_queryset(self):
        """Retrieve all active Appointments for Patient and Counselor"""
        queryset = Appointment.objects.filter(patient__is_active=True, counselor__is_active=True)

        # Update is_active status for each appointment
        for appointment in queryset:
            appointment.update_is_active()

        return queryset

    def create(self, request, *args, **kwargs):
        """Create new Appointment"""
        patient = request.data.get('patient')
        counselor = request.data.get('counselor')
        appointment_date = request.data.get('appointment_date')

        # check if the patient is active
        patient = Patient.objects.filter(patient_id=patient)
        if patient.exists():
            patient = patient.first()
            if not patient.is_active:
                return Response({'detail': 'This is not an active Patient'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No such Patient found'}, status=status.HTTP_400_BAD_REQUEST)

        # check if the patient is active
        counselor = Counselor.objects.filter(patient_id=patient)
        if counselor.exists():
            counselor = counselor.first()
            if not counselor.is_active:
                return Response({'detail': 'This is not an active Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No such Counselor found'}, status=status.HTTP_400_BAD_REQUEST)

        # check if the patient and counselor already have an active appointment
        active_appointments = Appointment.objects.filter(patient_id=patient, counselor_id=counselor, is_active=True)
        if active_appointments.exists():
            return Response({'detail': 'Patient and counselor already have an active appointment'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Update is_active status for the new appointment
        serializer.instance.update_is_active()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """Update existing Appointment"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Check if the patient is active
        patient = Patient.objects.filter(patient_id=request.data.get('patient'))
        if patient.exists():
            patient = patient.first()
            if not patient.is_active:
                return Response({'detail': 'This is not an active Patient'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No such Patient found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the counselor is active
        counselor = Counselor.objects.filter(patient_id=request.data.get('counselor'))
        if counselor.exists():
            counselor = counselor.first()
            if not counselor.is_active:
                return Response({'detail': 'This is not an active Counselor'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No such Counselor found'}, status=status.HTTP_400_BAD_REQUEST)

        appointment_date = request.data.get('appointment_date')
        if appointment_date:
            instance.appointment_date = appointment_date

            # Update is_active status if appointment_date has changed
            instance.update_is_active()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete for Appointment objects.
        Instead of actually deleting the object, set the `is_active` field to False.
        """
        instance = self.get_object()

        # Set is_active to False to deactivate the appointment
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
