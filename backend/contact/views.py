from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import ContactMessage
import re

class ContactMessageView(APIView):
    """
    Endpoint for submitting a contact message.
    """
    def post(self, request):
        name = request.data.get('name', '').strip()
        email = request.data.get('email', '').strip()
        subject = request.data.get('subject', '').strip()
        message = request.data.get('message', '').strip()
        honeypot = request.data.get('website', '')
        
        if honeypot:
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
            
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        cache_key = f"contact_limit_{ip}"
        if cache.get(cache_key):
             return Response({'error': 'You have submitted a message recently. Please wait a while before sending another.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
             
        if not name or not email or not subject or not message:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if len(message) > 5000:
            return Response({'error': 'Message is too long. Max 5000 characters.'}, status=status.HTTP_400_BAD_REQUEST)
            
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
             return Response({'error': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)
             
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        cache.set(cache_key, True, 3600)
        
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
