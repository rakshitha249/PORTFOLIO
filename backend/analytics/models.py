from django.db import models
from projects.models import Project

class PortfolioEvent(models.Model):
    EVENT_TYPES = [
        ('project_view', 'Project View'),
        ('github_view', 'GitHub View'),
        ('contact_submit', 'Contact Submit'),
        ('page_view', 'Page View')
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='analytics_events')
    path = models.CharField(max_length=255, blank=True)
    ip_hash = models.CharField(max_length=64, blank=True, help_text="Anonymized hash to count unique visitors without PII")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
        ]
        
    def __str__(self):
        return f"{self.event_type} at {self.created_at}"
