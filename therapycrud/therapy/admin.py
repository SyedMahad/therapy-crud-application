from django.contrib import admin
from .models import User, Patient, Counselor, Appointment


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active']

class CounselorAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'counselor', 'appointment_date', 'is_active']


admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Counselor, CounselorAdmin)
admin.site.register(Appointment, AppointmentAdmin)