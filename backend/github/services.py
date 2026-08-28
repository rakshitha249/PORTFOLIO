import json
import urllib.request
import urllib.error
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class GithubService:
    CACHE_KEY = 'github_repositories'
    CACHE_TTL = 3600  # 1 hour

    @staticmethod
    def get_repositories():
        cached_repos = cache.get(GithubService.CACHE_KEY)
        if cached_repos is not None:
            return cached_repos

        username = getattr(settings, 'GITHUB_USERNAME', None)
        token = getattr(settings, 'GITHUB_TOKEN', None)

        if not username:
            logger.error("GITHUB_USERNAME not configured")
            return []

        url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
        
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        if token:
            req.add_header('Authorization', f'token {token}')

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    
                    repos = []
                    for repo in data:
                        repos.append({
                            'id': repo.get('id'),
                            'name': repo.get('name', ''),
                            'description': repo.get('description', '') or '',
                            'html_url': repo.get('html_url', ''),
                            'homepage': repo.get('homepage', '') or '',
                            'language': repo.get('language', '') or '',
                            'topics': repo.get('topics', []),
                            'stargazers_count': repo.get('stargazers_count', 0),
                            'forks_count': repo.get('forks_count', 0),
                            'visibility': repo.get('visibility', 'public'),
                            'created_at': repo.get('created_at', ''),
                            'updated_at': repo.get('updated_at', ''),
                        })
                    
                    cache.set(GithubService.CACHE_KEY, repos, GithubService.CACHE_TTL)
                    return repos
                else:
                    logger.error(f"GitHub API returned status {response.status}")
                    return []
        except urllib.error.URLError as e:
            logger.error(f"Failed to fetch from GitHub: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error fetching from GitHub: {e}")
            return []
