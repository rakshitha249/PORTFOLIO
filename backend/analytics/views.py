from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
import hashlib
from .models import PortfolioEvent
from projects.models import Project

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hash_ip(ip):
    if not ip:
        return ""
    from django.conf import settings
    salt = getattr(settings, 'SECRET_KEY', 'default-salt')
    return hashlib.sha256(f"{ip}{salt}".encode('utf-8')).hexdigest()

class AnalyticsSummaryView(APIView):
    """
    Returns aggregate analytics data.
    """
    def get(self, request):
        total_project_views = PortfolioEvent.objects.filter(event_type='project_view').count()
        total_github_views = PortfolioEvent.objects.filter(event_type='github_view').count()
        total_contacts = PortfolioEvent.objects.filter(event_type='contact_submit').count()
        
        # Most viewed projects
        most_viewed = PortfolioEvent.objects.filter(event_type='project_view', project__isnull=False) \
            .values('project__title', 'project__slug') \
            .annotate(views=Count('id')) \
            .order_by('-views')[:5]
            
        return Response({
            'total_project_views': total_project_views,
            'total_github_views': total_github_views,
            'total_contacts': total_contacts,
            'most_viewed_projects': list(most_viewed)
        })

class AnalyticsTrackView(APIView):
    """
    Endpoint for the frontend to record non-intrusive analytics events.
    """
    def post(self, request):
        event_type = request.data.get('event_type')
        project_slug = request.data.get('project_slug')
        path = request.data.get('path', '')
        
        valid_event_types = [choice[0] for choice in PortfolioEvent.EVENT_TYPES]
        if event_type not in valid_event_types:
             return Response({'error': 'Invalid event_type'}, status=status.HTTP_400_BAD_REQUEST)
             
        ip_hash = hash_ip(get_client_ip(request))
        
        recent_events = PortfolioEvent.objects.filter(
            ip_hash=ip_hash,
            created_at__gte=timezone.now() - timedelta(hours=1)
        ).count()
        
        if recent_events > 100:
            return Response({'error': 'Rate limit exceeded'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
        project = None
        if project_slug:
            try:
                project = Project.objects.get(slug=project_slug)
            except Project.DoesNotExist:
                pass
                
        PortfolioEvent.objects.create(
            event_type=event_type,
            project=project,
            path=path[:255],
            ip_hash=ip_hash
        )
        
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
