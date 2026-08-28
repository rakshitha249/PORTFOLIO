from rest_framework.views import APIView
from rest_framework.response import Response
from .services import GithubService
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class RepositoryListView(APIView):
    """
    API endpoint that returns the public GitHub repositories.
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='language', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Filter by primary language'),
            OpenApiParameter(name='topic', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Filter by topic'),
            OpenApiParameter(name='search', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Search in repository name or description'),
            OpenApiParameter(name='sort', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Sort by "stars", "updated", or "alphabetical". Default is "updated".'),
            OpenApiParameter(name='limit', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, description='Limit the number of results returned'),
        ]
    )
    def get(self, request):
        repos = GithubService.get_repositories()
        
        # Filtering
        language = request.query_params.get('language')
        topic = request.query_params.get('topic')
        search = request.query_params.get('search')
        sort = request.query_params.get('sort', 'updated')
        limit = request.query_params.get('limit')
        
        if language:
            repos = [r for r in repos if r.get('language') and r['language'].lower() == language.lower()]
            
        if topic:
            repos = [r for r in repos if topic.lower() in [t.lower() for t in r.get('topics', [])]]
            
        if search:
            search_lower = search.lower()
            repos = [r for r in repos if search_lower in r.get('name', '').lower() or search_lower in r.get('description', '').lower()]
            
        # Sorting
        if sort == 'stars':
            repos.sort(key=lambda x: x.get('stargazers_count', 0), reverse=True)
        elif sort == 'alphabetical':
            repos.sort(key=lambda x: x.get('name', '').lower())
        else: # updated
            repos.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
            
        # Limit
        if limit:
            try:
                limit = int(limit)
                repos = repos[:limit]
            except ValueError:
                pass
                
        return Response(repos)
