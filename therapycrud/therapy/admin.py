from django.contrib import admin
from .models import User, Patient, Counselor, Appointment


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type']
    search_fields = ['username', 'email', 'user_type']

class PatientAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active']
    search_fields = ['username', 'is_active']

class CounselorAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_active']
    search_fields = ['username', 'is_active']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'counselor', 'appointment_date', 'is_active']
    search_fields = ['patient', 'counselor', 'appointment_date', 'is_active']


admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Counselor, CounselorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
