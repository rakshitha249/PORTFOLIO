from rest_framework import mixins, viewsets
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
