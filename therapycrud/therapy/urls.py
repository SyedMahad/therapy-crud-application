from django.urls import path, include
from rest_framework import routers

from .views import PatientViewSet, CounselorViewSet

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'counselors', CounselorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
