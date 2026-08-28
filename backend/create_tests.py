import os

files = {
    'projects/tests.py': """from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project, ProjectTechnology, ProjectMetric

class ProjectTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = Project.objects.create(
            title="AI Assistant",
            slug="ai-assistant",
            short_description="An AI chatbot",
            full_description="Detailed description here.",
            is_published=True,
            category="AI"
        )
        self.tech = ProjectTechnology.objects.create(project=self.project, name="Python")
        self.metric = ProjectMetric.objects.create(project=self.project, name="Accuracy", value="99%")

    def test_model_relationships(self):
        self.assertEqual(self.project.technologies.count(), 1)
        self.assertEqual(self.project.metrics.count(), 1)
        self.assertEqual(self.project.technologies.first().name, "Python")

    def test_api_list_projects(self):
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "AI Assistant")

    def test_api_retrieve_project_by_slug(self):
        url = reverse('project-detail', kwargs={'slug': self.project.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "AI Assistant")
        
    def test_project_filtering(self):
        url = reverse('project-list') + '?category=AI'
        response = self.client.get(url)
        self.assertEqual(len(response.data['results']), 1)
        
        url_empty = reverse('project-list') + '?category=Web'
        response_empty = self.client.get(url_empty)
        self.assertEqual(len(response_empty.data['results']), 0)
""",
    'contact/tests.py': """from django.test import TestCase
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
"""
}

for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Created all test files.")
