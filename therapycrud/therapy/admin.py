from django.contrib import admin
from .models import User, Patient, Counselor, Appointment

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active']

    def __str__(self):
        return self.user.username

class CounselorAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active']

    def __str__(self):
        return self.user.username

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'counselor', 'appointment_date', 'is_active']

    def __str__(self):
        return f"{self.patient.user.username}'s appointment with {self.counselor.user.username}"

admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Counselor, CounselorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
