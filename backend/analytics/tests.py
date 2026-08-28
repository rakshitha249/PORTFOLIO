from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import PortfolioEvent
from projects.models import Project

class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            short_description="Test Description",
            full_description="Full description",
            is_published=True
        )

    def test_track_event(self):
        url = reverse('analytics-track')
        data = {
            'event_type': 'project_view',
            'project_slug': 'test-project',
            'path': '/projects/test-project'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PortfolioEvent.objects.count(), 1)
        
        event = PortfolioEvent.objects.first()
        self.assertEqual(event.event_type, 'project_view')
        self.assertEqual(event.project, self.project)
        self.assertTrue(bool(event.ip_hash))

    def test_invalid_event_type(self):
        url = reverse('analytics-track')
        data = {'event_type': 'invalid_type'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_summary_endpoint(self):
        PortfolioEvent.objects.create(event_type='project_view', project=self.project)
        PortfolioEvent.objects.create(event_type='github_view')
        
        url = reverse('analytics-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_project_views'], 1)
        self.assertEqual(response.data['total_github_views'], 1)
        self.assertEqual(len(response.data['most_viewed_projects']), 1)
