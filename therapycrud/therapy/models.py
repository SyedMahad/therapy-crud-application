from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

import choices
import constants


class User(AbstractUser):
    """ Custom user model with email as the unique identifier and a user_type field """

    email = models.EmailField(unique=True)
    user_type = models.CharField(choices=choices.USER_CHOICES, max_length=16)

    # Set the email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    # Required fields for creating a user
    REQUIRED_FIELDS = ['username', 'password']

class GeneralManager(models.Manager):
    """ General manager to filter users based on user_type """

    def __init__(self, type=None):
        super(GeneralManager, self).__init__()
        self.user_type = type

    def get_queryset(self):
        # Override the get_queryset method to filter based on user_type
        return super(GeneralManager, self).get_queryset().filter(user_type=self.user_type)

class Patient(User):
    """ Proxy model for patient users """

    TYPE = constants.USER_TYPE_PATIENT
    objects = GeneralManager(type=TYPE)

    def save(self , *args , **kwargs):
        # Set the user_type field to the patient type
        self.user_type = self.TYPE
        return super().save(*args , **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        proxy = True

class Counselor(User):
    """ Proxy model for counselor users """

    TYPE = constants.USER_TYPE_COUNSELOR
    objects = GeneralManager(type=TYPE)

    def save(self , *args , **kwargs):
        # Set the user_type field to the counselor type
        self.user_type = self.TYPE
        return super().save(*args , **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        proxy = True

class Appointment(models.Model):
    """ Model for appointments with patient, counselor, appointment date, and is_active fields """

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointment')
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='counselor_appointment')
    appointment_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.patient.username}'s appointment with {self.counselor.username}"

    def update_is_active(self):
        # Method to update the is_active field based on the appointment date
        now = timezone.now()
        if self.appointment_date < now:
            self.is_active = False
        else:
            self.is_active = True
        self.save()
