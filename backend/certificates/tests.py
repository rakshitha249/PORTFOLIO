from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Certificate

class CertificateTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_seeded_certificates_exist(self):
        # We expect exactly 4 certificates to be seeded by the data migration
        self.assertEqual(Certificate.objects.count(), 4)

    def test_api_list_certificates(self):
        url = reverse('certificate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check results in the paginated response
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 4)

        # Ensure relative credential_urls are dynamically resolved to absolute URIs
        for cert in results:
            self.assertTrue(cert['credential_url'].startswith('http://testserver/'))
