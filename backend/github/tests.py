from django.test import TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.core.cache import cache

class GithubTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch('urllib.request.urlopen')
    @override_settings(GITHUB_USERNAME='testuser', GITHUB_TOKEN='')
    def test_get_repositories(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"id": 1, "name": "test-repo", "description": "Test", "html_url": "url", "homepage": "", "language": "Python", "topics": ["test"], "stargazers_count": 5, "forks_count": 1, "created_at": "2023", "updated_at": "2024"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        url = reverse('github-repositories')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'test-repo')

    @patch('urllib.request.urlopen')
    @override_settings(GITHUB_USERNAME='testuser')
    def test_github_api_failure(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 403
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        url = reverse('github-repositories')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
