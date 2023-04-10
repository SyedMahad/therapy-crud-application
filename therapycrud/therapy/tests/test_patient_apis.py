from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from therapy.models import Patient


User = get_user_model()

class TestPatientViewSet(APITestCase):

    def setUp(self):
        # Create a superuser for testing purposes
        self.admin_user = User.objects.create_superuser(
            username='test_admin_user', 
            email='test_admin_user@example.com', 
            password='test_admin_pass'
        )

        # Authenticate the client using the superuser credentials
        self.authenticate()

        # Create a Patient instance for testing
        self.patient = Patient.objects.create(
            username='test',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            is_active=True
        )

    def authenticate(self):
        """
        Helper method to authenticate an admin user and set the credentials on the test client.
        """
        # Construct data dictionary containing the admin user's email and password
        data = {
            "email": self.admin_user.email,
            "password": self.admin_user.password
        }

        # Obtain a token for the admin user
        token = self.client.post(reverse_lazy('token_obtain_pair'), data)
        token = RefreshToken.for_user(self.admin_user)

        # Set the token in the Authorization header of the test client's requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))

        # Force authentication of the test client as the admin user
        self.client.force_authenticate(user=self.admin_user)

    def test_list_patients(self):
        # Send a GET request to the 'patient-list' endpoint
        response = self.client.get(reverse_lazy('patient-list'))

        # Ensure that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_create_patient(self):
        # Define the data for the new patient
        data = {
            'email': 'johndoe@example.com',
            'username': 'johndoe',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        # Send a POST request to create the new patient using the patient-list endpoint
        response = self.client.post(reverse_lazy('patient-list'), data)

        # Assert that the request was successful and the patient was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the number of patients in the database is now 2
        # one is the Patient we created for this class
        # two is the Patient we created for this method
        self.assertEqual(Patient.objects.count(), 2)

        # Assert that the attributes of the created patient match the provided data
        patient = Patient.objects.last()
        self.assertEqual(patient.email, 'johndoe@example.com')
        self.assertEqual(patient.username, 'johndoe')
        self.assertEqual(patient.user_type, 'patient')
        self.assertEqual(patient.first_name, 'John')
        self.assertEqual(patient.last_name, 'Doe')

    def test_delete_patient(self):
        # Send a DELETE request to the patient detail endpoint with the patient's id
        response = self.client.delete(reverse_lazy('patient-detail', args=[self.patient.id]))

        # Check that the response status code is 204 (No Content)
        self.assertEqual(response.status_code, 204)

        # Check that the patient with the specified id is no longer active in the database
        self.assertFalse(Patient.objects.filter(id=self.patient.id, is_active=True).exists())
