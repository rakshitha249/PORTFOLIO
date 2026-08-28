from rest_framework import viewsets
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
