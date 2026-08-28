import os

files = {
    'portfolio/serializers.py': """from rest_framework import serializers
from .models import Profile, Skill, SocialLink

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'
""",
    'portfolio/views.py': """from rest_framework import viewsets
from .models import Profile, Skill, SocialLink
from .serializers import ProfileSerializer, SkillSerializer, SocialLinkSerializer

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class SocialLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
""",
    'projects/serializers.py': """from rest_framework import serializers
from .models import Project, ProjectTechnology, ProjectMetric

class ProjectTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTechnology
        fields = ['id', 'name']

class ProjectMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMetric
        fields = ['id', 'name', 'value']

class ProjectSerializer(serializers.ModelSerializer):
    technologies = ProjectTechnologySerializer(many=True, read_only=True)
    metrics = ProjectMetricSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
""",
    'projects/views.py': """from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
""",
    'experience/serializers.py': """from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
""",
    'experience/views.py': """from rest_framework import viewsets
from .models import Experience
from .serializers import ExperienceSerializer

class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
""",
    'education/serializers.py': """from rest_framework import serializers
from .models import Education

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
""",
    'education/views.py': """from rest_framework import viewsets
from .models import Education
from .serializers import EducationSerializer

class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
""",
    'certificates/serializers.py': """from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'
""",
    'certificates/views.py': """from rest_framework import viewsets
from .models import Certificate
from .serializers import CertificateSerializer

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
""",
    'contact/serializers.py': """from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
""",
    'contact/views.py': """from rest_framework import mixins, viewsets
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
""",
    'config/urls.py': """from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from portfolio.views import ProfileViewSet, SkillViewSet, SocialLinkViewSet
from projects.views import ProjectViewSet
from experience.views import ExperienceViewSet
from education.views import EducationViewSet
from certificates.views import CertificateViewSet
from contact.views import ContactMessageViewSet

router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'social-links', SocialLinkViewSet, basename='sociallink')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'experience', ExperienceViewSet, basename='experience')
router.register(r'education', EducationViewSet, basename='education')
router.register(r'certificates', CertificateViewSet, basename='certificate')
router.register(r'contact', ContactMessageViewSet, basename='contact')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
"""
}

for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Created all serializers, views, and urls.")
