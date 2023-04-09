from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User, Patient, Counselor, Appointment
from .serializers import UserSerializer, PatientSerializer, CounselorSerializer, AppointmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class CounselorViewSet(viewsets.ModelViewSet):
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.filter(patient__is_active=True, counselor__is_active=True)
        for appointment in queryset:
            appointment.update_is_active()
        return queryset

    def create(self, request, *args, **kwargs):
        patient = request.data.get('patient')
        counselor = request.data.get('counselor')
        appointment_date = request.data.get('appointment_date')

        # check if the patient and counselor already have an active appointment
        active_appointments = Appointment.objects.filter(patient_id=patient, counselor_id=counselor, is_active=True)
        if active_appointments.exists():
            return Response({'detail': 'Patient and counselor already have an active appointment'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer.instance.update_is_active()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        appointment_date = request.data.get('appointment_date')
        if appointment_date:
            instance.appointment_date = appointment_date
            instance.update_is_active()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
