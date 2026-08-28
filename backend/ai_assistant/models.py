import hashlib
from django.db import models
from django.conf import settings

def is_postgres():
    engine = settings.DATABASES['default']['ENGINE']
    return 'postgresql' in engine or 'postgis' in engine

class KnowledgeDocument(models.Model):
    SOURCE_CHOICES = [
        ('profile', 'Profile'),
        ('skill', 'Skill'),
        ('project', 'Project'),
        ('education', 'Education'),
        ('experience', 'Experience'),
        ('certification', 'Certification'),
        ('github', 'GitHub'),
    ]

    title = models.CharField(max_length=255)
    source_type = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    source_id = models.CharField(max_length=255)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    content_hash = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('source_type', 'source_id')
        indexes = [
            models.Index(fields=['source_type', 'source_id']),
            models.Index(fields=['content_hash']),
        ]

    def __str__(self):
        return f"{self.source_type} - {self.title}"

    def save(self, *args, **kwargs):
        if self.content:
            self.content_hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)


class KnowledgeChunk(models.Model):
    document = models.ForeignKey(KnowledgeDocument, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    chunk_index = models.IntegerField()
    metadata = models.JSONField(default=dict, blank=True)
    content_hash = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    if is_postgres():
        from pgvector.django import VectorField
        embedding = VectorField(dimensions=768, null=True, blank=True)
    else:
        embedding = models.JSONField(null=True, blank=True, help_text="Fallback for SQLite")

    class Meta:
        ordering = ['document', 'chunk_index']
        indexes = [
            models.Index(fields=['document', 'chunk_index']),
        ]

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"

    def save(self, *args, **kwargs):
        if self.content:
            self.content_hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)
