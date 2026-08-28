from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import ContactMessage
from django.core.cache import cache

class ContactTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('contact-submit')
        cache.clear()

    def test_valid_submission(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Hello',
            'message': 'This is a test message.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_honeypot_spam_protection(self):
        data = {
            'name': 'Spammer',
            'email': 'spam@example.com',
            'subject': 'Spam',
            'message': 'Buy my stuff',
            'website': 'http://spam.com' # Honeypot field filled
        }
        response = self.client.post(self.url, data, format='json')
        # Should return 201 to fool the bot, but not save
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_rate_limiting(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Hello',
            'message': 'Message 1'
        }
        # First submission works
        response1 = self.client.post(self.url, data, format='json', REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Second submission fails due to rate limit
        response2 = self.client.post(self.url, data, format='json', REMOTE_ADDR='127.0.0.1')
        self.assertEqual(response2.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_invalid_email(self):
        data = {
            'name': 'John',
            'email': 'not-an-email',
            'subject': 'Hi',
            'message': 'Test'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContactMessage.objects.count(), 0)
