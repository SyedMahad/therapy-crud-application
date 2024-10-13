from django.urls import path, include
from rest_framework import routers

from .views import (
    UserViewSet,
    PatientViewSet,
    CounselorViewSet,
    AppointmentViewSet,
    RegisterView,
    CustomTokenObtainPairView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'counselors', CounselorViewSet, basename='counselor')
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
]
