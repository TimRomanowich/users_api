from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
# Create your tests here.

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('api-register')  

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])