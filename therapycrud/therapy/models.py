from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

import choices
import constants


class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(choices=choices.USER_CHOICES, max_length=16)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

class GeneralManager(models.Manager):
    def __init__(self, type=None):
        super(GeneralManager, self).__init__()
        self.user_type = type

    def get_queryset(self):
        return super(GeneralManager, self).get_queryset().filter(user_type=self.user_type)

class Patient(User):
    TYPE = constants.USER_TYPE_PATIENT
    objects = GeneralManager(type=TYPE)

    def __str__(self):
        return self.username

    class Meta:
        proxy = True

class Counselor(User):
    TYPE = constants.USER_TYPE_COUNSELOR
    objects = GeneralManager(type=TYPE)

    def __str__(self):
        return self.username

    class Meta:
        proxy = True

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointment')
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='counselor_appointment')
    appointment_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patient.username}'s appointment with {self.counselor.username}"

    def update_is_active(self):
        now = timezone.now()
        if self.appointment_date < now:
            self.is_active = False
        else:
            self.is_active = True
        self.save()
