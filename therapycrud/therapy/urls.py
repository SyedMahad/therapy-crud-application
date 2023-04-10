from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, PatientViewSet, CounselorViewSet, AppointmentViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'counselors', CounselorViewSet)
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
