from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from portfolio.views import ProfileViewSet, SkillViewSet, SocialLinkViewSet
from projects.views import ProjectViewSet
from experience.views import ExperienceViewSet
from education.views import EducationViewSet
from certificates.views import CertificateViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'social-links', SocialLinkViewSet, basename='sociallink')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'education', EducationViewSet, basename='education')
router.register(r'certificates', CertificateViewSet, basename='certificate')
from .views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/github/', include('github.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
