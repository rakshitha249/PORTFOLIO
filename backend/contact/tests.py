from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import ContactMessage

class ContactTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('contact-list')

    def test_create_contact_message(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Hello",
            "message": "This is a test message."
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_validation(self):
        # Missing email should fail validation
        data = {
            "name": "John Doe",
            "subject": "Hello",
            "message": "No email provided."
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
