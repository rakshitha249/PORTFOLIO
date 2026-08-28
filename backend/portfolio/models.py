from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    resume_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50, help_text="0 to 100")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or identifier")

    def __str__(self):
        return self.platform
